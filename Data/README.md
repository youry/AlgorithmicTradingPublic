## General Information

This folder contains stock, bond, index, and commodity data from:

1) July 1, 2019 to December 30, 2022

2) July 1, 2023 to October 24, 2025 

The raw datasets were extracted from the [Financial Model Prep (FMP) API](https://site.financialmodelingprep.com/developer/docs).

---
# Financial Model Prep (FMP) API Guide

Use the following API template to access the extended 5-min interval datasets from a specified time range: 
`
https://financialmodelingprep.com/api/v3/historical-chart/5min/{symbol}?from={year-month-day}&to={year-month-day}&extended=true&apikey={your_api_key}
`

Example (5 min): https://financialmodelingprep.com/api/v3/historical-chart/5min/AAPL?from=2023-07-01&to=2025-06-30&extended=true&apikey=secret

To collect data at a different custom interval, adjust the interval in the API as shown in the following example (15-minute interval): https://financialmodelingprep.com/api/v3/historical-chart/15min/AAPL?from=2023-07-01&to=2025-06-30&extended=true&apikey=secret

Make sure to use "extended=true" to include pre-market and post-market data in the datasets, as explained in [FMP's FAQ section](https://site.financialmodelingprep.com/faqs?search=does_the_intraday_historical_market_cover_pre-market_and_after_hours?).

About Stock Data Timezone: "In general, the time zone for the endpoints corresponds to the country/region the exchange is located in. For example, stocks traded on the NYSE are on the EST time zone, and stocks traded on the London Stock Exchange (LSE) correspond to the GMT zone." - [FMP FAQ](https://site.financialmodelingprep.com/faqs?search=whatisthetimezoneforcommoditiessymbols)

About Commodity Data Timezone: "It's EST (Eastern Standard Time) is the time zone for the eastern part of the United States and Canada, which is 5 hours behind Coordinated Universal Time (UTC-5)." - [FMP FAQ](https://site.financialmodelingprep.com/faqs?search=whatisthetimezoneforcommoditiessymbols)

29 Stock Symbols: {"AAPL", "AMD", "AMZN", "BA", "BABA", "BAC", "C", "CSCO", "CVX", "DIS", "F", "GE", "GOOGL", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "META", "MSFT", "NFLX", "NVDA", "PFE", "T", "TSLA", "VZ", "WMT", "XOM"}

503 Stock Symbols: {"A", "AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM", "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", "ALB", "ALGN", "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", "AMT", "AMZN", "ANET", "AON", "AOS", "APA", "APD", "APH", "APO", "APP", "APTV", "ARE", "ATO", "AVB", "AVGO", "AVY", "AWK", "AXON", "AXP", "AZO", "BA", "BABA", "BAC", "BALL", "BAX", "BBY", "BEN", "BDX", "BF.B", "BG", "BIIB", "BK", "BKNG", "BKR", "BLDR", "BLK", "BMY", "BR", "BRK.B", "BRO", "BSX", "BX", "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", "CBRE", "CCI", "CCL", "CDNS", "CDW", "CEG", "CF", "CFG", "CHD", "CHRW", "CHTR", "CI", "CINF", "CL", "CLX", "CMCSA", "CME", "CMG", "CMI", "CMS", "CNC", "CNP", "COF", "COIN", "COO", "COP", "COR", "COST", "CPAY", "CPB", "CPRT", "CPT", "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX", "CTAS", "CTRA", "CTSH", "CTVA", "CVS", "CVX", "D", "DAL", "DASH", "DAY", "DD", "DDOG", "DE", "DECK", "DELL", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", "DOC", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA", "DVN", "DXCM", "EA", "EBAY", "ECL", "ED", "EFX", "EG", "EIX", "EL", "ELV", "EME", "EMN", "EMR", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ERIE", "ES", "ESS", "ETN", "ETR", "EVRG", "EW", "EXC", "EXE", "EXPD", "EXPE", "EXR", "F", "FANG", "FAST", "FCX", "FDS", "FDX", "FE", "FFIV", "FI", "FICO", "FITB", "FISV", "FOX", "FOXA", "FRT", "FSLR", "FTNT", "FTV", "GD", "GDDY", "GE", "GEHC", "GEN", "GEV", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOGL", "GPC", "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", "HIG", "HII", "HLT", "HOLX", "HON", "HOOD", "HPE", "HPQ", "HRL", "HSIC", "HST", "HSY", "HUBB", "HUM", "HWM", "IBKR", "IBM", "ICE", "IDXX", "IEX", "IFF", "INCY", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM", "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JBL", "JCI", "JKHY", "JNJ", "JPM", "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KMB", "KMI", "KMX", "KKR", "KLAC", "KO", "KR", "KVUE", "L", "LDOS", "LEN", "LH", "LHX", "LII", "LIN", "LKQ", "LLY", "LMT", "LNT", "LOW", "LRCX", "LULU", "LUV", "LW", "LVS", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", "MCK", "MCO", "MDLZ", "MDT", "MET", "META", "MGM", "MHK", "MKC", "MLM", "MMC", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR", "MRNA", "MRK", "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ", "NDSN", "NEE", "NEM", "NFLX", "NI", "NKE", "NOC", "NOW", "NRG", "NSC", "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWS", "NWSA", "NXPI", "O", "ODFL", "OKE", "OMC", "ON", "ORCL", "ORLY", "OTIS", "OXY", "PANW", "PAYC", "PAYX", "PCAR", "PCG", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", "PKG", "PLD", "PLTR", "PM", "PNC", "PNR", "PNW", "PODD", "POOL", "PPG", "PPL", "PRU", "PSA", "PSKY", "PSX", "PTC", "PWR", "PYPL", "QCOM", "RCL", "REG", "REGN", "RF", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", "RSG", "RTX", "RVTY", "SBAC", "SBUX", "SCHW", "SHW", "SJM", "SLB", "SMCI", "SNA", "SNPS", "SO", "SOLV", "SPG", "SPGI", "SRE", "STE", "STLD", "STT", "STX", "STZ", "SW", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", "TDG", "TDY", "TECH", "TEL", "TER", "TFC", "TGT", "TJX", "TKO", "TMO", "TMUS", "TPL", "TPR", "TRGP", "TRMB", "TROW", "TRV", "TSCO", "TSLA", "TSN", "TT", "TTD", "TTWO", "TXN", "TXT", "TYL", "UAL", "UBER", "UDR", "UHS", "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V", "VICI", "VLO", "VLTO", "VMC", "VRSK", "VRSN", "VRTX", "VST", "VTR", "VTRS", "VZ", "WAB", "WAT", "WBD", "WDAY", "WDC", "WEC", "WELL", "WFC", "WM", "WMB", "WMT", "WRB", "WSM", "WST", "WTW", "WY", "WYNN", "XEL", "XOM", "XYL", "XYZ", "YUM", "ZBH", "ZBRA", "ZTS"}

Bond Symbols: {"^IRX", "^FVX", "^TNX"}

Index Symbols: {"^DJI", "^IXIC", "^GSPC"}

Commodity Symbols: {"GC=F", "CL=F"}

### FMP Excel Add-On

Use the function "FMP.HISTORICALCHART()" to access historical data.

Here is an example that accesses extended 5-min interval data for Apple: 

`
=FMP.HISTORICALCHART("AAPL","5min", "2023-07-01","2025-10-23", ,TRUE)
`

This command ended up accessing data from October 14, 2025 to October 23, 2025; it did not access the specified time range.

Trying to run "Automated" Scripts gives the following error:

	"The workbook and script belong to different organizations"

The Excel workbook and the Office Script are stored in different organizational accounts, which prevents the script from being executed. To resolve this, both the workbook and the script need to be shared within the same organization or account. Support: https://support.microsoft.com/en-gb/office/sharing-office-scripts-in-excel-226eddbc-3a44-4540-acfe-fccda3d1122b

### Datasets to Collect - July 1, 2023 to October 23, 2025 

(see [Financial Model Prep (FMP) API](https://site.financialmodelingprep.com/developer/docs). 
Account name: khmelevsky@gmail.com passord (ask youry))

- [ ] 29 Stocks
- [ ] 3 Bonds (13 Week Treasury, 5 Year Treasury, 10 Year Treasury)
- [ ] 3 Indices (Dow Jones, NASDAQ, S&P 500)
- [ ] 2 Commodities (Gold, Crude Oil)

(Changed from 2 Year Treasury to 13 Week Treasury)

# Historical Data to Purchase #
1. https://firstratedata.com/b/17/etf-complete-historical-intraday 
Frequency	Date Range	Number of Tickers	
Buy Now $572.95 CAD
1-minute,
5-minute,
30-minute,
1-hour,
1-day
Jan 2000 - Sep 2025
4289 Tickers
   
---
## Link from Previous Phase ##

Ionos.com HiDrive for the data https://hidrive.ionos.com/share/n2ur5c.qv0#login
