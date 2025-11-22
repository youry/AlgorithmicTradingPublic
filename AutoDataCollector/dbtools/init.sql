-- This init.sql script is for setting up the remote DB to work with Auto Data Collector
CREATE SCHEMA IF NOT EXISTS market;

-- 29 stock tickers
CREATE TABLE IF NOT EXISTS market.aapl  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.amd   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.amzn  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.ba    (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.baba  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.bac   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.c     (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.csco  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.cvx   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.dis   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.f     (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.ge    (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.googl (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.ibm   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.intc  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.jnj   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.jpm   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.ko    (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.mcd   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.meta  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.msft  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.nflx  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.nvda  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.pfe   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.t     (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.tsla  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.vz    (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.wmt   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.xom   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);

-- Index and Comoditys
CREATE TABLE IF NOT EXISTS market.ixic  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.gspc  (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.dji   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.gcf   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);
CREATE TABLE IF NOT EXISTS market.clf   (ts timestamp PRIMARY KEY, open numeric(18,6), high numeric(18,6), low numeric(18,6), close numeric(18,6), volume bigint);

-- Job history table for trackinsg runs
CREATE TABLE IF NOT EXISTS market.jobhistory (
    id serial PRIMARY KEY,
    jobname text NOT NULL,
    ts timestamp NOT NULL,
    status text NOT NULL
);
