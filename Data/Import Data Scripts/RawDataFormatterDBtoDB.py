import psycopg2
import pandas as pd
import holidays
from io import StringIO

from functools import reduce

from numpy.f2py.auxfuncs import throw_error


def main():

    #ALL 503 STOCKS MUST USE UNDERSCORE '_' instead of DOT '.' FOR ANY TICKERS IN LIST
    stockTickers = [
        'A','AAPL','ABBV','ABNB','ABT','ACGL','ACN','ADBE','ADI','ADM',
        'ADP','ADSK','AEE','AEP','AES','AFL','AIG','AIZ','AJG','AKAM',
        'ALB','ALGN','ALL','ALLE','AMAT','AMCR','AMD','AME','AMGN','AMP',
        'AMT','AMZN','ANET','AON','AOS','APA','APD','APH','APO','APP',
        'APTV','ARE','ATO','AVB','AVGO','AVY','AWK','AXON','AXP','AZO',
        'BA','BABA','BAC','BALL','BAX','BBY','BEN','BDX','BF_B','BG',
        'BIIB','BK','BKNG','BKR','BLDR','BLK','BMY','BR','BRK_B','BRO',
        'BSX','BX','BXP','C','CAG','CAH','CARR','CAT','CB','CBOE','CBRE',
        'CCI','CCL','CDNS','CDW','CEG','CF','CFG','CHD','CHRW','CHTR','CI',
        'CINF','CL','CLX','CMCSA','CME','CMG','CMI','CMS','CNC','CNP',
        'COF','COIN','COO','COP','COR','COST','CPAY','CPB','CPRT','CPT',
        'CRL','CRM','CRWD','CSCO','CSGP','CSX','CTAS','CTRA','CTSH','CTVA',
        'CVS','CVX','D','DAL','DASH','DAY','DD','DDOG','DE','DECK','DELL',
        'DG','DGX','DHI','DHR','DIS','DLR','DLTR','DOC','DOV','DOW','DPZ',
        'DRI','DTE','DUK','DVA','DVN','DXCM','EA','EBAY','ECL','ED','EFX',
        'EG','EIX','EL','ELV','EME','EMN','EMR','EOG','EPAM','EQIX','EQR',
        'EQT','ERIE','ES','ESS','ETN','ETR','EVRG','EW','EXC','EXE',
        'EXPD','EXPE','EXR','F','FANG','FAST','FCX','FDS','FDX','FE',
        'FFIV','FISV','FICO','FITB','FIS','FOX','FOXA','FRT','FSLR','FTNT',
        'FTV','GD','GDDY','GE','GEHC','GEN','GEV','GILD','GIS','GL','GLW',
        'GM','GNRC','GOOGL','GPC','GPN','GRMN','GS','GWW','HAL','HAS',
        'HBAN','HCA','HD','HIG','HII','HLT','HOLX','HON','HOOD','HPE','HPQ',
        'HRL','HSIC','HST','HSY','HUBB','HUM','HWM','IBKR','IBM','ICE','IDXX',
        'IEX','IFF','INCY','INTC','INTU','INVH','IP','IPG','IQV','IR','IRM',
        'ISRG','IT','ITW','IVZ','J','JBHT','JBL','JCI','JKHY','JNJ','JPM',
        'K','KDP','KEY','KEYS','KHC','KIM','KMB','KMI','KMX','KKR','KLAC',
        'KO','KR','KVUE','L','LDOS','LEN','LH','LHX','LII','LIN','LKQ','LLY',
        'LMT','LNT','LOW','LRCX','LULU','LUV','LW','LVS','LYB','LYV','MA',
        'MAA','MAR','MAS','MCD','MCHP','MCK','MCO','MDLZ','MDT','MET','META',
        'MGM','MHK','MKC','MLM','MMC','MMM','MNST','MO','MOH','MOS','MPC',
        'MPWR','MRNA','MRK','MS','MSCI','MSFT','MSI','MTB','MTCH','MTD','MU',
        'NCLH','NDAQ','NDSN','NEE','NEM','NFLX','NI','NKE','NOC','NOW','NRG',
        'NSC','NTAP','NTRS','NUE','NVDA','NVR','NWS','NWSA','NXPI','O','ODFL',
        'OKE','OMC','ON','ORCL','ORLY','OTIS','OXY','PANW','PAYC','PAYX',
        'PCAR','PCG','PEG','PEP','PFE','PFG','PG','PGR','PH','PHM','PKG','PLD',
        'PLTR','PM','PNC','PNR','PNW','PODD','POOL','PPG','PPL','PRU','PSA',
        'PSKY','PSX','PTC','PWR','PYPL','QCOM','RCL','REG','REGN','RF','RJF',
        'RL','RMD','ROK','ROL','ROP','ROST','RSG','RTX','RVTY','SBAC','SBUX',
        'SCHW','SHW','SJM','SLB','SMCI','SNA','SNPS','SO','SOLV','SPG','SPGI',
        'SRE','STE','STLD','STT','STX','STZ','SW','SWK','SWKS','SYF','SYK',
        'SYY','T','TAP','TDG','TDY','TECH','TEL','TER','TFC','TGT','TJX','TKO',
        'TMO','TMUS','TPL','TPR','TRGP','TRMB','TROW','TRV','TSCO','TSLA','TSN',
        'TT','TTD','TTWO','TXN','TXT','TYL','UAL','UBER','UDR','UHS','ULTA',
        'UNH','UNP','UPS','URI','USB','V','VICI','VLO','VLTO','VMC','VRSK','VRSN',
        'VRTX','VST','VTR','VTRS','VZ','WAB','WAT','WBD','WDAY','WDC','WEC','WELL',
        'WFC','WM','WMB','WMT','WRB','WSM','WST','WTW','WY','WYNN','XEL','XOM',
        'XYL','XYZ','YUM','ZBH','ZBRA','ZTS'
    ]

    #LIST STILL NEEDED TO RUN ON youry_db FOR FIX. HAS OTHER 501 STOCKS ALREADY
    # stockTickers = ["BF_B", "BRK_B"]

    cursor = 0
    #Connect to localhost:15432 (the tunnel endpoint)
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=15432,
            database="database",
            user="user",
            password="pass"
        )
        cursor = conn.cursor()

    except psycopg2.Error as e:
        print("Could not connect to database")
        exit(44)



    #sector dataframe creation finished here
    #
    # #sector dataframe not currently used but should be used instead of hard coding

    commodityTickers = ["IRX", "FVX", "TNX", "DJI", "IXIC", "GSPC", "GCF", "CLF"]
    #Commodities Dataframes created and added to dictionary from database
    commoditiesDataFrames = {}
    for commodity in commodityTickers:
        commoditiesDataFrames[commodity] = get_stocks_as_dataframe(commodity,cursor)
        commoditiesDataFrames[commodity].drop_duplicates(subset=['date'], keep='first', inplace=True)
        commoditiesDataFrames[commodity].rename(columns={'date': 'Time'}, inplace=True)
        commoditiesDataFrames[commodity].rename(columns={'close': 'Close'}, inplace=True)
        (commoditiesDataFrames[commodity])['DATETIME'] = pd.to_datetime((commoditiesDataFrames[commodity])['Time'], format='%Y-%m-%d %H:%M:%S')


    #Maps real table names to Appropriate names for model columns
    commodityTickerColumns = {"IRX": "US13W",
                              "FVX": "US5Y",
                              "TNX": "US10Y",
                              "DJI": "DJ",
                              "IXIC": "NQ",
                              "GSPC": "SP",
                              "GCF": "Gold",
                              "CLF": "Oil"}

    commodities_reduced = []
    # rename column Date to Time
    for commodity in commodityTickers:
        plainCommodityName = commodityTickerColumns[commodity]
        commodities_reduced.append(commoditiesDataFrames[commodity].filter(['Close', 'DATETIME']). \
                                   rename(columns={'Close': '{}_PP'.format(plainCommodityName)}))

    merge_commodities = reduce(lambda df1, df2: pd.merge(df1, df2, on='DATETIME'), commodities_reduced)

    stocks_reduced = []
    for ticker in stockTickers:

        stock = get_stocks_as_dataframe(ticker, cursor)

        if not stock.empty:
            print(f"Retrieved {len(stock)} rows for {ticker}")
        else:
            print(f"No data found for {ticker}")
            continue

        #NEED TO REVIEW NAMES FROM DATABASE TO SEE IF THIS MAKES SENSE
        stock.rename(columns={"close": "Close"}, inplace=True)
        stock.rename(columns={"volume": "Volume_PP"}, inplace=True)
        stock["Symbol"] = ticker

        stock.drop_duplicates(subset=['date'], keep='first', inplace=True)
        stock['DATETIME'] = pd.to_datetime(stock["date"], format='%Y-%m-%d %H:%M:%S')

        stocks_reduced.append(stock.filter(["Symbol", "Close", "Volume_PP", 'DATETIME']))


    merged_df = []
    for stock in stocks_reduced:
        merged_df.append(pd.merge(stock, merge_commodities, on="DATETIME"))



    #Adds dataframes rows to the end of each other to make a long dataframes of all rows for each stock
    df = reduce(lambda df1, df2: pd.concat([df1, df2], ignore_index=True), merged_df)

    df = merge_sectors_dataframe(df,cursor) # Merges Sectors into the Merged_df

    print("Sectors Merged")

    # create columns for each categorical datetime variable of interest
    df['DATE'] = df.DATETIME.dt.date
    df['MONTH'] = df.DATETIME.dt.month
    df['DAY'] = df.DATETIME.dt.day
    df['HOUR'] = df.DATETIME.dt.hour
    df['MINUTE'] = df.DATETIME.dt.minute
    df['WEEK_DAY'] = df.DATETIME.dt.dayofweek

    # Create holiday flag
    holiday_days = []
    for holiday in holidays.US(state='NY', years=[2023, 2024, 2025]).items(): holiday_days.append(str(holiday[0]))
    df['HOLIDAY'] = [1 if str(value) in holiday_days else 0 for value in df['DATE']]

    # Create pre - post holiday flag
    df['POSTHOLIDAY_MORNING'], df['PREHOLIDAY_AFTERNOON'] = 0, 0

    id = df.loc[(df.HOLIDAY == 1), :].index
    POSTHOLIDAY = pd.to_datetime((df.loc[id, 'DATE'] + pd.DateOffset(days=1)).unique())
    PREHOLIDAY = pd.to_datetime((df.loc[id, 'DATE'] - pd.DateOffset(days=1)).unique())

    for i in range(len(PREHOLIDAY)): df.loc[(df.DATE == PREHOLIDAY[i]) & (df.HOUR > 12), 'PREHOLIDAY_AFTERNOON'] = 1

    for i in range(len(POSTHOLIDAY)): df.loc[
        (df.DATE == POSTHOLIDAY[i]) & (df.HOUR <= 12), 'POSTHOLIDAY_MORNING'] = 1

    # Create monday morning flag
    df['MONDAY_MORNING'] = 0
    df.loc[(df.WEEK_DAY == 0) & (df.HOUR <= 12), 'MONDAY_MORNING'] = 1

    # Create friday afternoon flag
    df['FRIDAY_AFTERNOON'] = 0
    df.loc[(df.WEEK_DAY == 4) & (df.HOUR > 12), 'FRIDAY_AFTERNOON'] = 1

    # Delete holiday days
    df.drop(df.index[df['HOLIDAY'] == 1], inplace=True)
    df.drop(columns=['HOLIDAY'], inplace=True)

    print("Handled Holidays")

    to_encode = ['WEEK_DAY', 'MINUTE', 'HOUR', 'MONTH', 'DAY', 'Sector']

    encoded_df = df
    for encode in to_encode:
        encoded_df = one_hot(encoded_df, encode)

    print("Hot Encoded Data")
    encoded_df = encoded_df.replace({True: 1, False: 0})
    print("changed booleans flags to integers")
    encoded_df = encoded_df.drop(['DATE'], axis=1)
    print("Dropped Date Column")

    encoded_df["Volume_PP"] = encoded_df["Volume_PP"].astype(int)
    print("Changed Volume_PP to integers")

    encoded_df['Symbol'] = encoded_df['Symbol'].str.replace('_', '.', regex=False)

    # Backup to csv if insertion into database fails
    try:
        store_model_data(encoded_df,cursor)
    except Exception as e:
        print(e)
        encoded_df.to_csv('./output/ModelDatasetFormatTemp.csv', index=False)


    print("Data has been stored")

#End of Main
    # cursor.close()
    # conn.close()



def one_hot(og_df, feature_to_encode):
    "Function that takes a dataframe, and a feature to one-hot encode and returns the dataframe with that feature encoded"
    dummies = pd.get_dummies(og_df[feature_to_encode], prefix = feature_to_encode, prefix_sep = "_")
    df = pd.concat([og_df, dummies], axis=1)
    df = df.drop([feature_to_encode], axis=1)
    return df


def get_stocks_as_dataframe(ticker,cursor):

    # #temp check using csv
    # directory = "./input/"
    # return pd.read_csv(directory + ticker + ".csv")

    try:
        cursor.execute(f"""
                       SELECT date, open, high, low, close, volume
                       FROM market.{ticker}
                       """)

        # Fetch all results
        results = cursor.fetchall()

        # Get column names from cursor description
        columns = [desc[0].lower() for desc in cursor.description]

        # Create DataFrame
        df = pd.DataFrame(results, columns=columns)


        return df

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error

def store_model_data(df, cursor):
    print("attempting to read csv in chunks")

    try:

        #Type casting safety before insert
        df['Close'] = df['Close'].astype(float)
        df['Volume_PP'] = df['Volume_PP'].astype('uint64')
        df['US13W_PP'] = df['US13W_PP'].astype(float)
        df['US5Y_PP'] = df['US5Y_PP'].astype(float)
        df['US10Y_PP'] = df['US10Y_PP'].astype(float)
        df['DJ_PP'] = df['DJ_PP'].astype(float)
        df['NQ_PP'] = df['NQ_PP'].astype(float)
        df['SP_PP'] = df['SP_PP'].astype(float)
        df['Gold_PP'] = df['Gold_PP'].astype(float)
        df['Oil_PP'] = df['Oil_PP'].astype(float)

        # Convert boolean columns
        bool_columns = [
            'POSTHOLIDAY_MORNING', 'PREHOLIDAY_AFTERNOON', 'MONDAY_MORNING', 'FRIDAY_AFTERNOON',
            'WEEK_DAY_0', 'WEEK_DAY_1', 'WEEK_DAY_2', 'WEEK_DAY_3', 'WEEK_DAY_4',
            'MINUTE_0', 'MINUTE_15', 'MINUTE_30', 'MINUTE_45', 'HOUR_9', 'HOUR_10',
            'HOUR_11', 'HOUR_12', 'HOUR_13', 'HOUR_14', 'MONTH_1', 'MONTH_2', 'MONTH_3',
            'MONTH_4', 'MONTH_5', 'MONTH_6', 'MONTH_7', 'MONTH_8', 'MONTH_9', 'MONTH_10',
            'MONTH_11', 'MONTH_12', 'DAY_1', 'DAY_2', 'DAY_3', 'DAY_4', 'DAY_5', 'DAY_6',
            'DAY_7', 'DAY_8', 'DAY_9', 'DAY_10', 'DAY_11', 'DAY_12', 'DAY_13', 'DAY_14',
            'DAY_15', 'DAY_16', 'DAY_17', 'DAY_18', 'DAY_19', 'DAY_20', 'DAY_21', 'DAY_22',
            'DAY_23', 'DAY_24', 'DAY_25', 'DAY_26', 'DAY_27', 'DAY_28', 'DAY_29', 'DAY_30',
            'DAY_31', 'Sector_Basic_Materials', 'Sector_Communication_Services',
            'Sector_Consumer_Cyclical', 'Sector_Consumer_Defensive', 'Sector_Energy',
            'Sector_Financial_Services', 'Sector_Healthcare', 'Sector_Industrials',
            'Sector_Real_Estate', 'Sector_Technology', 'Sector_Utilities'
        ]

        #Error checking for Hot Encoding limitations for small stock list Transformation and insertion
        for col in bool_columns:
            if col not in df.columns:
                df[col] = 0

        #Type casting safety before insert
        for col in bool_columns:
            df[col] = df[col].astype(bool)

        # Ensure DATETIME is in proper format
        df['DATETIME'] = pd.to_datetime(df['DATETIME'])

        print("Data prepared. About to insert using COPY...")

        # Use StringIO for in-memory copy
        buffer = StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)

        cursor.copy_expert("""
            COPY market.ModelFeatures (Symbol,Close,Volume_PP,DATETIME,US13W_PP,US5Y_PP,US10Y_PP,DJ_PP,NQ_PP,SP_PP,Gold_PP,Oil_PP,POSTHOLIDAY_MORNING,PREHOLIDAY_AFTERNOON,MONDAY_MORNING,FRIDAY_AFTERNOON,WEEK_DAY_0,WEEK_DAY_1,WEEK_DAY_2,WEEK_DAY_3,WEEK_DAY_4,MINUTE_0,MINUTE_5,MINUTE_10,MINUTE_15,MINUTE_20,MINUTE_25,MINUTE_30,MINUTE_35,MINUTE_40,MINUTE_45,MINUTE_50,MINUTE_55,HOUR_9,HOUR_10,HOUR_11,HOUR_12,HOUR_13,HOUR_14,MONTH_1,MONTH_2,MONTH_3,MONTH_4,MONTH_5,MONTH_6,MONTH_7,MONTH_8,MONTH_9,MONTH_10,MONTH_11,MONTH_12,DAY_1,DAY_2,DAY_3,DAY_4,DAY_5,DAY_6,DAY_7,DAY_8,DAY_9,DAY_10,DAY_11,DAY_12,DAY_13,DAY_14,DAY_15,DAY_16,DAY_17,DAY_18,DAY_19,DAY_20,DAY_21,DAY_22,DAY_23,DAY_24,DAY_25,DAY_26,DAY_27,DAY_28,DAY_29,DAY_30,DAY_31,Sector_Basic_Materials,Sector_Communication_Services,Sector_Consumer_Cyclical,Sector_Consumer_Defensive,Sector_Energy,Sector_Financial_Services,Sector_Healthcare,Sector_Industrials,Sector_Real_Estate,Sector_Technology,Sector_Utilities
            ) FROM STDIN WITH CSV HEADER
        """, buffer)

        cursor.connection.commit()
        print(f"COPY finished - inserted {len(df)} rows")

    except psycopg2.Error as e:
        cursor.connection.rollback()
        print(f"Insert Error: {e}")
    except Exception as e:
        cursor.connection.rollback()
        print(f"Unexpected Error: {e}")
        raise Exception("Insert Error: Backing up to csv instead")


def merge_sectors_dataframe(merged_df,cursor):

    sector_df = pd.DataFrame()
    try:
        cursor.execute("""
                       SELECT Symbol, Sector
                       FROM market.Sectors
                       """)

        # Fetch all results
        results = cursor.fetchall()

        # Get column names from cursor description
        columns = [desc[0].lower() for desc in cursor.description]

        # Create DataFrame
        sector_df = pd.DataFrame(results, columns=columns)

        sector_df.columns = sector_df.columns.str.capitalize()

        sector_df = sector_df.replace({'Symbol': {'\.': '_'}}, regex=True)

    except psycopg2.Error as e:
        print(f"Database error: {e}")

    # sector_df = pd.read_csv("./output/SectorFixedList.csv")
    # print(sector_df.loc[sector_df['Symbol'] == 'BF_B', ['Symbol', 'Sector']])
    # input("Wait")
    merged_df = merged_df.merge(sector_df, on='Symbol')
    # print(merged_df.loc[merged_df['Symbol'] == 'BF_B', ['Symbol', 'Sector']])
    # input("Wait")
    return merged_df



if __name__ == "__main__":
    main()