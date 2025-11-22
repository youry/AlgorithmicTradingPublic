import csv
from datetime import datetime, timedelta

# Stock List
# stocks = ["A", "AAPL", "ABBV", "ABNB", "ABT", "ACGL", "ACN", "ADBE", "ADI", "ADM", 
#          "ADP", "ADSK", "AEE", "AEP", "AES", "AFL", "AIG", "AIZ", "AJG", "AKAM", 
#          "ALB", "ALGN", "ALL", "ALLE", "AMAT", "AMCR", "AMD", "AME", "AMGN", "AMP", 
#          "AMT", "AMZN", "ANET", "AON", "AOS", "APA", "APD", "APH", "APO", "APP", 
#          "APTV", "ARE", "ATO", "AVB", "AVGO", "AVY", "AWK", "AXON", "AXP", "AZO", 
#          "BA", "BABA", "BAC", "BALL", "BAX", "BBY", "BEN", "BDX", "BF.B", "BG", 
#          "BIIB", "BK", "BKNG", "BKR", "BLDR", "BLK", "BMY", "BR", "BRK.B", "BRO", 
#          "BSX", "BX", "BXP", "C", "CAG", "CAH", "CARR", "CAT", "CB", "CBOE", 
#          "CBRE", "CCI", "CCL", "CDNS", "CDW", "CEG", "CF", "CFG", "CHD", "CHRW", 
#          "CHTR", "CI", "CINF", "CL", "CLX", "CMCSA", "CME", "CMG", "CMI", "CMS", 
          
#          "CNC", "CNP", "COF", "COIN", "COO", "COP", "COR", "COST", "CPAY", "CPB", 
#          "CPRT", "CPT", "CRL", "CRM", "CRWD", "CSCO", "CSGP", "CSX", "CTAS", "CTRA", 
#          "CTSH", "CTVA", "CVS", "CVX", "D", "DAL", "DASH", "DAY", "DD", "DDOG", 
#          "DE", "DECK", "DELL", "DG", "DGX", "DHI", "DHR", "DIS", "DLR", "DLTR", 
#          "DOC", "DOV", "DOW", "DPZ", "DRI", "DTE", "DUK", "DVA", "DVN", "DXCM", 
#          "EA", "EBAY", "ECL", "ED", "EFX", "EG", "EIX", "EL", "ELV", "EME", 
#          "EMN", "EMR", "EOG", "EPAM", "EQIX", "EQR", "EQT", "ERIE", "ES", "ESS", 
#          "ETN", "ETR", "EVRG", "EW", "EXC", "EXE", "EXPD", "EXPE", "EXR", "F", 
#          "FANG", "FAST", "FCX", "FDS", "FDX", "FE", "FFIV", "FI", "FICO", "FITB", 
#          "FIS", "FOX", "FOXA", "FRT", "FSLR", "FTNT", "FTV", "GD", "GDDY", "GE", 
          
#          "GEHC", "GEN", "GEV", "GILD", "GIS", "GL", "GLW", "GM", "GNRC", "GOOGL", 
#          "GPC", "GPN", "GRMN", "GS", "GWW", "HAL", "HAS", "HBAN", "HCA", "HD", 
#          "HIG", "HII", "HLT", "HOLX", "HON", "HOOD", "HPE", "HPQ", "HRL", "HSIC", 
#          "HST", "HSY", "HUBB", "HUM", "HWM", "IBKR", "IBM", "ICE", "IDXX", "IEX", 
#          "IFF", "INCY", "INTC", "INTU", "INVH", "IP", "IPG", "IQV", "IR", "IRM", 
#          "ISRG", "IT", "ITW", "IVZ", "J", "JBHT", "JBL", "JCI", "JKHY", "JNJ", 
#          "JPM", "K", "KDP", "KEY", "KEYS", "KHC", "KIM", "KMB", "KMI", "KMX", 
#          "KKR", "KLAC", "KO", "KR", "KVUE", "L", "LDOS", "LEN", "LH", "LHX", 
#          "LII", "LIN", "LKQ", "LLY", "LMT", "LNT", "LOW", "LRCX", "LULU", "LUV", 
#          "LW", "LVS", "LYB", "LYV", "MA", "MAA", "MAR", "MAS", "MCD", "MCHP", 
          
#          "MCK", "MCO", "MDLZ", "MDT", "MET", "META", "MGM", "MHK", "MKC", "MLM", 
#          "MMC", "MMM", "MNST", "MO", "MOH", "MOS", "MPC", "MPWR", "MRNA", "MRK", 
#          "MS", "MSCI", "MSFT", "MSI", "MTB", "MTCH", "MTD", "MU", "NCLH", "NDAQ", 
#          "NDSN", "NEE", "NEM", "NFLX", "NI", "NKE", "NOC", "NOW", "NRG", "NSC", 
#          "NTAP", "NTRS", "NUE", "NVDA", "NVR", "NWS", "NWSA", "NXPI", "O", "ODFL", 
#          "OKE", "OMC", "ON", "ORCL", "ORLY", "OTIS", "OXY", "PANW", "PAYC", "PAYX", 
#          "PCAR", "PCG", "PEG", "PEP", "PFE", "PFG", "PG", "PGR", "PH", "PHM", 
#          "PKG", "PLD", "PLTR", "PM", "PNC", "PNR", "PNW", "PODD", "POOL", "PPG", 
#          "PPL", "PRU", "PSA", "PSKY", "PSX", "PTC", "PWR", "PYPL", "QCOM", "RCL", 
#          "REG", "REGN", "RF", "RJF", "RL", "RMD", "ROK", "ROL", "ROP", "ROST", 
          
#          "RSG", "RTX", "RVTY", "SBAC", "SBUX", "SCHW", "SHW", "SJM", "SLB", "SMCI", 
#          "SNA", "SNPS", "SO", "SOLV", "SPG", "SPGI", "SRE", "STE", "STLD", "STT", 
#          "STX", "STZ", "SW", "SWK", "SWKS", "SYF", "SYK", "SYY", "T", "TAP", 
#          "TDG", "TDY", "TECH", "TEL", "TER", "TFC", "TGT", "TJX", "TKO", "TMO", 
#          "TMUS", "TPL", "TPR", "TRGP", "TRMB", "TROW", "TRV", "TSCO", "TSLA", "TSN", 
#          "TT", "TTD", "TTWO", "TXN", "TXT", "TYL", "UAL", "UBER", "UDR", "UHS", 
#          "ULTA", "UNH", "UNP", "UPS", "URI", "USB", "V", "VICI", "VLO", "VLTO", 
#          "VMC", "VRSK", "VRSN", "VRTX", "VST", "VTR", "VTRS", "VZ", "WAB", "WAT", 
#          "WBD", "WDAY", "WDC", "WEC", "WELL", "WFC", "WM", "WMB", "WMT", "WRB", 
#          "WSM", "WST", "WTW", "WY", "WYNN", "XEL", "XOM", "XYL", "XYZ", "YUM", 
          
#          "ZBH", "ZBRA", "ZTS"]

stocks = ["A", "ABBV", "ABNB", "ABT"]

holidays = ["2023-07-04",
"2023-09-04",
"2023-11-23",
"2023-12-25",
"2024-01-01",
"2024-01-15",
"2024-02-19",
"2024-03-29",
"2024-05-27",
"2024-06-19",
"2024-07-04",
"2024-09-02",
"2024-11-28",
"2024-12-25",
"2025-01-01",
"2025-01-09",
"2025-01-20",
"2025-02-17",
"2025-04-18",
"2025-05-26",
"2025-06-19",
"2025-07-04",
"2025-09-01"]

early_close_dates = [datetime(2023,7,3).date(),
datetime(2023,11,24).date(),
datetime(2024,7,3).date(),
datetime(2024,11,29).date(),
datetime(2024,12,24).date(),
datetime(2025,7,3).date()]

early_close_time = timedelta(hours=13)

holiday_dates = set(datetime.strptime(h, "%Y-%m-%d").date() for h in holidays)

for stock in stocks:
    # Load CSV
    with open(stock + ".csv", newline='') as f:
        reader = csv.DictReader(f)
        actual_timestamps = set()
        for row in reader:
            dt = datetime.strptime(row['date'], "%Y-%m-%d %H:%M:%S")
            actual_timestamps.add(dt)

    # Trading hours
    market_open = timedelta(hours=9, minutes=30)
    market_close = timedelta(hours=16, minutes=0)

    # Date range
    start_date = datetime(2023, 7, 1).date()
    end_date = datetime(2025, 10, 24).date()

    total_missing = 0

    # Formatting for console printing
    print()
    print(f"######## Starting {stock} ########")

    current = start_date
    while current <= end_date:
        if current.weekday() < 5 and current not in holiday_dates:
            # Generate expected 5-minute intervals for this day
            t = datetime.combine(current, datetime.min.time()) + market_open
            if current in early_close_dates:
                end_dt = datetime.combine(current, datetime.min.time()) + early_close_time
            else:
                end_dt = datetime.combine(current, datetime.min.time()) + market_close
            while t < end_dt:
                if t not in actual_timestamps:
                    print(f"Missing {stock} on: {t}")
                    total_missing += 1
                t += timedelta(minutes=5)
        current += timedelta(days=1)

    # Results
    print(f"Total missing 5-minute intervals for {stock}: {total_missing}")
    print()
