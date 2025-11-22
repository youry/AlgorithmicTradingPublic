# Coverage test for auto collector
# Designed to be started via auto_collector.timer and run once after each market day
# Coverage expectation increases each market day for complete coverage percentage of
# data collection since its start
import os
import datetime as dt
import psycopg2
import re
import logging
from zoneinfo import ZoneInfo

LOG_DIR = "/home/almalinux/AlgorithmicTrading/AutoDataCollector/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = f"{LOG_DIR}/AutoCollection_{dt.datetime.now():%Y-%m-%d}.log"

file_handler = logging.FileHandler(LOG_FILE, mode="a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(message)s"))

logger = logging.getLogger("coverage_test")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Use EST
MARKET_TZ = ZoneInfo("America/New_York")

# Set this date to the day auto collection started
START_DATE = dt.date(2025, 11, 14) # was at 11/12 before im temporairly switching it to today for my interview
TODAY = dt.date.today()

# Db Connection info
DB_HOST = os.getenv("PGHOST")
DB_PORT = int(os.getenv("PGPORT"))
DB_NAME = os.getenv("PGDATABASE")
DB_USER = os.getenv("PGUSER")
DB_PASS = os.getenv("PGPASSWORD")

# Symbols to evaluate
SYMBOLS = [s.strip() for s in os.getenv("SYMBOLS", "AAPL,MSFT,GOOG").split(",") if s.strip()]

def connect():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )

# Returns expected data entries in a single market day (78 entries)
def expected_intervals_per_day():
    start = dt.datetime(2025, 1, 1, 9, 30)
    end = dt.datetime(2025, 1, 1, 16, 0)
    return int((end - start).total_seconds() / 300)

# clean symbol name to match db tables
def format_table_name(symbol):
    clean = re.sub(r"[^A-Za-z0-9]", "", symbol).lower()
    clean = symbol.lower().replace('-', '_').replace('.', '_')
    return f"market.{clean}"

# find coverage for a single symbol
def coverage_for_symbol(conn, symbol, start_date, end_date):
    table = format_table_name(symbol)
    expected_per_day = expected_intervals_per_day()
    total_expected = 0
    total_actual = 0
    with conn.cursor() as cur:
        current_date = start_date
        while current_date <= end_date:
            if current_date.weekday() >= 5:
                current_date += dt.timedelta(days=1)
                continue
            open_dt = dt.datetime.combine(current_date, dt.time(9, 30), tzinfo=MARKET_TZ).replace(tzinfo=None)
            close_dt = dt.datetime.combine(current_date, dt.time(16, 0), tzinfo=MARKET_TZ).replace(tzinfo=None)
            total_expected += expected_per_day
            try:
                cur.execute(
                    f"SELECT COUNT(*) FROM {table} WHERE ts >= %s AND ts < %s AND EXTRACT(HOUR FROM ts) BETWEEN 9 AND 15",
                    (open_dt, close_dt),
                )
                count = cur.fetchone()[0]
                total_actual += count
            except Exception:
                raise RuntimeError(f"Table query failed for {table}")
            current_date += dt.timedelta(days=1)
    if total_expected == 0:
        return 0.0, total_actual, total_expected
    coverage = round((total_actual / total_expected) * 100, 2)
    return coverage, total_actual, total_expected


# coverage test start
def run_coverage_test():
    conn = connect()
    logger.info(f"\nFull Data Coverage Report ({START_DATE} → {TODAY})")
    logger.info("-" * 50)
    print(f"\nFull Data Coverage Report ({START_DATE} → {TODAY})\n{'-'*50}")
    total_coverage = 0
    symbol_count = 0
    # get coverage for each symbol 
    for sym in SYMBOLS:
        try:
            coverage, actual, expected = coverage_for_symbol(conn, sym, START_DATE, TODAY)
            total_coverage += coverage
            symbol_count += 1
            line = f"{sym:<6} → {coverage:>6.2f}%  ({actual} / {expected})"
        except Exception as e:
            line = f"{sym:<6} → error: {e}"
        logger.info(line)
        print(line)
    # compute the average coverage for all symbols
    avg_coverage = (total_coverage / symbol_count) if symbol_count else 0
    summary = f"\nOverall Coverage: {avg_coverage:.2f}%\n"
    logger.info(summary)
    print(summary)
    logger.info("End of Full Coverage Report\n")
    for h in logger.handlers:
        h.flush()
    conn.close()

# entry point
if __name__ == "__main__":
    run_coverage_test()
