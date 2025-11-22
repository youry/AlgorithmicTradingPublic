# Auto Data Collector Script
# Meant to be ran via run_collector.sh 
# Running this script should collect data for the last hour with 5 mintues extra overlap
import os
import re
import sys
import time
import datetime as dt
import requests
import logging
import psycopg2
import traceback
from psycopg2.extras import execute_values
from concurrent.futures import ThreadPoolExecutor, as_completed
from zoneinfo import ZoneInfo

# Environment config
API_KEY = os.getenv("FMP_API_KEY", "")
DB_HOST = os.getenv("PGHOST")
DB_PORT = int(os.getenv("PGPORT"))
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASS = os.getenv("PGPASSWORD")

STOCK_SYMBOLS = [s.strip() for s in os.getenv("SYMBOLS", "AAPL").split(",") if s.strip()]
INDEX_SYMBOLS = [s.strip() for s in os.getenv("INDEX_SYMBOLS", "").split(",") if s.strip()]
COMMODITY_SYMBOLS = [s.strip() for s in os.getenv("COMMODITY_SYMBOLS", "").split(",") if s.strip()]

MARKET_TZ = ZoneInfo(os.getenv("MARKET_TZ", "America/New_York")) # EST

WINDOW_MINUTES = int(os.getenv("WINDOW_MINUTES", "60")) # 1 hour window
REQUEST_DELAY = float(os.getenv("API_DELAY_SECONDS", "0.1")) # delay in seconds to prevent FMP rate limiting
SYMBOL_LIMIT = 600  # change this to limit how many symbols we work with for testing

# Logging setup
# creates a log file for each day. records the outcome of each execution of this script
LOG_DIR = "/home/almalinux/AlgorithmicTrading/AutoDataCollector/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = f"{LOG_DIR}/AutoCollection_{dt.datetime.now():%Y-%m-%d}.log"

file_handler = logging.FileHandler(LOG_FILE, mode="a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter("%(message)s"))

logger = logging.getLogger("collector")
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

email_log =''

# Helper functions     

# Create DB connection 
def connect_to_database():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )

# Help cleanup timestamp from FMP
def parse_fmp_timestamp(timestamp_str: str):
    # cleaned up timestamp from FMP. FMP data is in EST
    clean_ts = dt.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=MARKET_TZ)
    # drop tzinfo from the timestamp to avoid postgres converting to UTC
    return clean_ts.replace(tzinfo=None)


# Get time window for data fetch
def get_current_time_window():    
    # Returns a rolling 1-hour EST window ending 5 minutes before current time
    ny_tz = ZoneInfo("America/New_York")
    now_ny = dt.datetime.now(ny_tz)

    # end 5 minutes before current time (to ensure last bar is finalized)
    end_time = now_ny.replace(second=0, microsecond=0) - dt.timedelta(minutes=20)
    start_time = end_time - dt.timedelta(hours=1)

    # drop tzinfo for DB storage (keeps EST local times)
    return start_time.replace(tzinfo=None), end_time.replace(tzinfo=None)


# This converts symbol string to corresponding DB table name
def format_table_name(symbol: str) -> str:
    # Normalize case and replace dash/dot for stock-style tickers
    clean = symbol.lower().replace('-', '_').replace('.', '_')

    # Remove any remaining characters that aren't letters, numbers, or underscores
    clean = re.sub(r'[^a-z0-9_]', '', clean)

    # Return schema-qualified name
    return f"market.{clean}"


# Help ensure given symbol string has a corresponding table name in the DB
def ensure_table_exists(conn, table_name: str):
    schema, table = table_name.split(".", 1)
    with conn.cursor() as cur:
        cur.execute(
            """SELECT 1 FROM information_schema.tables
               WHERE table_schema=%s AND table_name=%s""",
            (schema, table)
        )
        if not cur.fetchone():
            raise RuntimeError(f"Missing table: {table_name}")


# Fetch and insert data to DB for a single symbol 
def fetch_and_insert_data(conn, category, symbol, window_start, window_end) -> int:
    base_urls = {
        "Index": "https://financialmodelingprep.com/stable/historical-chart/5min?symbol={symbol}",
        "Commodity": "https://financialmodelingprep.com/stable/historical-chart/5min?symbol={symbol}",
        "Stock": "https://financialmodelingprep.com/api/v3/historical-chart/5min/{symbol}"
    }
    url = base_urls.get(category, base_urls["Stock"]).format(symbol=symbol)
    # url parameters for fmp api:
    params = {"from": window_start.strftime("%Y-%m-%d"),
              "to": window_end.strftime("%Y-%m-%d"),
              "extended": "true", "apikey": API_KEY}

    try:
        time.sleep(REQUEST_DELAY) # pause by set delay to avoid rate limiting FMP
        r = requests.get(url, params=params, timeout=15) # send API req for 5-min interval data for the whole day
        r.raise_for_status()
        data = r.json() if r.content else []  # data from FMP 
    except Exception as e:
        logger.debug(f"[{category}] {symbol} request failed: {e}")
        raise

    rows = []
    for record in data:
        ts = record.get("date")
        if not ts: # if no data skip
            continue
        
        ts_parsed = parse_fmp_timestamp(ts) # cleanup FMP timestamp
      
        # if data record from FMP is between our time window then append it rows
        if window_start <= ts_parsed < window_end and record.get("close") is not None:
            rows.append((ts_parsed, record.get("open"), record.get("high"),
                         record.get("low"), record.get("close"), record.get("volume")))

    table = format_table_name(symbol) # get table name from symbol
    ensure_table_exists(conn, table) # make sure table name is actually in the DB

    if not rows: # if FMP's response never had a record within the time range then log no data
        logger.debug(f"[{category}] {symbol} ... No data")
        return 0

    # UPSERT into corresponding table.
    # This tells postgres insert normally but if theres another row with the
    # same timestamp, do not insert a duplicate just update it instead
    # this should result in clean data hopefully
    insert_sql = f"""
        INSERT INTO {table} (ts, open, high, low, close, volume)
        VALUES %s
        ON CONFLICT (ts) DO UPDATE SET
            open=EXCLUDED.open, high=EXCLUDED.high,
            low=EXCLUDED.low, close=EXCLUDED.close, volume=EXCLUDED.volume;
    """
    with conn.cursor() as cur:
        execute_values(cur, insert_sql, rows) # run sql command 
    conn.commit()
    logger.debug(f"[{category}] {symbol} ... Upserted {len(rows)} rows")
    return len(rows)


# Our method to fetch and insert data from FMP by group (index, commodity, stock, ...)
def process_symbol_group(conn, symbols, category, window_start, window_end, max_workers=1) -> int:
    # Using concurrent.futures ThreadPoolExecutor in order to better handle lots of tickers
    # Since we have to make a seperate request to FMP for each symbol, fetching 500 tickers normally took forever

    # Instead of running the whole collection process sequentially,
    # ThreadPoolExecutor gives our fetch_and_insert_data() to a thread pool
    # where each thread can work on a different symbol all at the same time
    # this can make it too fast causing FMP rate limit, so we need to keep max_workers low
    # max_workers defines the amount of threads to use

    total_rows = 0
    symbols = symbols[:SYMBOL_LIMIT]
    print(f" Processing {len(symbols)} {category} symbols...")

    # Create the thread pool
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # the futures list will contain all submitted thread tasks
        futures = []
        for symbol in symbols: # create a future for each symbol
            future = executor.submit( 
                fetch_and_insert_data,  # function to run in background
                conn,                   # database connection
                category,               # category type (Stock, Index, Commodity)
                symbol,                 # the current symbol
                window_start,            # time window start
                window_end              # time window end
            )
            # store the future 
            futures.append(future)

        # wait for each background task to complete
        for future in as_completed(futures):
            try:
                # get total rows inserted from fetch_and_insert_data()
                rows_inserted = future.result()
                # add to complete row count
                total_rows += rows_inserted

            except Exception as e:
                raise RuntimeError(f"{category} symbol failed: {e}")

    # after all threads are done, return the total number of rows inserted
    return total_rows


# Record history of this job into jobhistory table 
def record_job_history(conn, status):
    timestamp = dt.datetime.now(MARKET_TZ)
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO market.jobhistory (jobname, ts, status) VALUES (%s, %s, %s)",
            ("Auto Data Collection", timestamp, status))
    conn.commit()

# Main - start of our auto collection
def main():
    
    print("Starting data collection")
    if not API_KEY:
        sys.exit("FMP_API_KEY is missing from environment variables.")
    
    # get time window we will use for this run
    window_start, window_end = get_current_time_window()
    print(f"Time window (EST): {window_start} → {window_end}")
    logger.info(f"[Collector] Window used EST: {window_start} → {window_end}")



    run_start = time.perf_counter()
    total_rows = 0
    failures = 0
    failure_details = []

    try:
        conn = connect_to_database()
    except Exception as e:
        failures += 1
        failure_details.append(("Database connection", e, traceback.format_exc()))
        conn = None

    if conn: # if db connects 
        for category, symbols in [("Index", INDEX_SYMBOLS),
                                  ("Commodity", COMMODITY_SYMBOLS),
                                  ("Stock", STOCK_SYMBOLS)]:
            try: # run data collection via proccess_symbol_group() for each category of asset
                total_rows += process_symbol_group(conn, symbols, category, window_start, window_end)
            except Exception as e:
                failures += 1 
                failure_details.append((f"{category} group", e, traceback.format_exc()))

        try: # insert execution result into jobhistory table in DB
            record_job_history(conn, "Good" if failures == 0 else "Fail")
        except Exception as e:
            failures += 1
            failure_details.append(("Job history insert", e, traceback.format_exc()))

        try:
            conn.close()
        except Exception:
            pass

    elapsed = time.perf_counter() - run_start # time it took to finish script for logging
    success = (failures == 0 and total_rows > 0) # log as success if no exceptions and some data is inserted

    # Add script result to the log file
    logger.info(f"Run complete | Duration={elapsed:.1f}s | Rows={total_rows} | Success={success}")
    print(f"Run complete | Duration={elapsed:.1f}s | Rows={total_rows} | Success={success}")

    # If the run failed due to exceptions
    if not success and failure_details:
        logger.error("-------- FAILURE DETAILS --------")
        email_log = "-------- FAILURE DETAILS --------\n"
        for context, err, tb in failure_details:
            logger.error(f"FAILURE in {context}: {err}")
            email_log += f"FAILURE in {context}: {err} \n"
            for line in tb.strip().splitlines():
                logger.error(line)
                email_log+=line + "\n"
        logger.error("-------- END FAILURE DETAILS --------")
        # this flush just makes it appear better in logs
        for h in logger.handlers:
            h.flush()

    # If no data inserted but no exception raised
    elif not success and total_rows == 0 and failures == 0:
        logger.error("-------- NO DATA INSERTED --------")
        logger.error("Run finished without errors but no rows were found or inserted.")
        logger.error("Probably due to time window outside of market hours")
        for h in logger.handlers:
            h.flush()    

# script entry point
if __name__ == "__main__":
    main()
