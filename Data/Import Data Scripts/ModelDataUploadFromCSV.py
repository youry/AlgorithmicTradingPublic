import psycopg2
import pandas as pd
from io import StringIO

def main():

    # Connect to localhost:15432 (the tunnel endpoint)
    conn = psycopg2.connect(
        host="localhost",
        port=15432,
        database="database",
        user="user",
        password="pass"
    )

    #Insertion Code
    cursor = conn.cursor()


    store_model_data(cursor)

    cursor.close()
    conn.close()


def store_model_data(cursor):
    print("attempting to read csv in chunks")

    chunkSizeRows = 1000000
    iter = 0
    for df in pd.read_csv("./output/ModelDatasetFormat.csv", chunksize=chunkSizeRows):
        print(f"Model Training {iter}: ")
        iter += 1

        try:
            # Just convert data types - no need to copy or reorder if CSV structure matches table
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

#End of Main
if __name__ == "__main__":
    main()


