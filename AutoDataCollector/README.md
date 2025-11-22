# Auto Data Collector (FMP → PostgreSQL)

## Overview
This system continuously collects 5-minute interval stock, index, and commodity price data from the Financial Modeling Prep (FMP) API and stores it into a PostgreSQL database.

The Auto Data Collector is designed to run within our Arbutus Cloud VM instance, where it operates as a background service managed by systemd timers. This setup ensures that market data is collected routinely and continuously throughout trading hours, maintaining hourly database updates for all tracked tickers

---

## How To Connect to DB

If you want to connect to the auto collector DB from your computer you first need a ssh key-pair set up for the project.

Once you have setup ssh then you can do ssh local port forwarding to connect to the postgres port secret using local port secret.

`ssh -L secret:127.0.0.1:secret almalinux@secretip`

Then try connecting to postgres using db connection info:
 - host: 127.0.0.1
 - username: secret
 - port: secret
 - database: secret
 


## System Design Summary
**ETL Pattern:** Extract → Load (no transformation)

| Step | Description |
|------|--------------|
| **Extract** | Fetches raw OHLCV (Open, High, Low, Close, Volume) data for each symbol from the FMP API. |
| **Load** | Inserts it directly into PostgreSQL tables named by symbol (e.g., `market.aapl`, `market.msft`) with **upsert logic**
| **Transform** | No transformation performed. Data is stored exactly as received from the API. |

---

## Timezones & Data Consistency
- **Market Timezone:** All timestamps are interpreted in **America/New_York (EST/EDT)**.
- **Database Storage:** Data is stored as timezone-stripped timestamps in EST to prevent PostgreSQL from converting to UTC.
- **Result:** Queries match the actual FMP timestamps exactly without shifting due to timezone conversions.

---

## How the collection works
1. **Fetch window determination:**  
   The (`data_collector.py`) script calculates a time window to choose which data to insert from the daily 5-min FMP API
   an extra 5 minute overlap allows to help collect the last data point for each hour in case it gets missed

2. **Parallel symbol fetching:**  
   Using Python’s concurrent.futures.ThreadPoolExecutor, symbols are fetched concurrently to improve throughput while respecting FMP rate limits

3. **Upsert into PostgreSQL:**  
   Each symbol’s data is inserted or updated based on its timestamp. Duplicate intervals are updated cleanly, preventing duplicates or gaps

4. **Hourly execution:**  
   A systemd timer should trigger the script at least once per hour in order to not miss any rows and have a continously updating DB

---

## Testing 
   The test script (`coverage_test.py`) is designed to be ran once daily at market close, checking data completeness across all tracked symbols and logging the results.

## Database Schema
Each symbol has its own table under the `market` schema, for example:
```sql
CREATE TABLE market.aapl (
  ts TIMESTAMP PRIMARY KEY,
  open  DOUBLE PRECISION,
  high  DOUBLE PRECISION,
  low   DOUBLE PRECISION,
  close DOUBLE PRECISION,
  volume BIGINT
);
