/*
 * File:        init.sql
 * Description: Implements the functionality for the MyModule library.
 * Author:      [Your Name/Team Name]
 * Date:        November 26, 2025
 * Version:     1.0.0
 * License:     MIT License (or other relevant license)
 *              Copyright (c) 2025 [Your Name/Organization]
 *
 *              Permission is hereby granted, free of charge, to any person obtaining a copy
 *              of this software and associated documentation files (the "Software"), to deal
 *              in the Software without restriction, including, without limitation, the rights
 *              to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 *              copies of the Software, and to permit persons to whom the Software is
 *              furnished to do so, subject to the following conditions:
 *
 *              The above copyright notice and this permission notice shall be included in all
 *              copies or substantial portions of the Software.
 *
 *              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 *              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 *              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 *              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 *              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 *              OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 *              SOFTWARE.
 */

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
