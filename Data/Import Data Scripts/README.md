# Historical Insertion into Database 
this directory contains scripts and explaination for the insertion method used for historical data into the fir database

All following instructions can be done after connecting to fir using the ssh tunnel with the -L flag (directions to connect show here: https://github.com/youry/AlgorithmicTrading/blob/main/DRIproject/README.md)

**FIR DATABASE NOTES:**

- **Current (patched) RawDataFormatterDBtoDB.py still needs to be run on youry_db for stock list ["BF_B", "BRK_B"]**
- **the 29 stocks tables (and ModelFeatures rows for their Symbol) in the following list are using the patched data which seems to be for a shorter period and in 15 minute intervals. ["AAPL", "AMD", "AMZN", "BA", "BABA", "BAC", "C", "CSCO", "CVX", "DIS", "F", "GE", "GOOGL", "IBM", "INTC", "JNJ", "JPM", "KO", "MCD", "META", "MSFT", "NFLX", "NVDA", "PFE", "T", "TSLA", "VZ", "WMT", "XOM"]** 



## Table Creation 

All tables that are created and needed can be made by running the .sql files found in this directory. This is necessary before running the following python scripts to insert data into the database if the tables have not already been created beforehand.

All tables created are on the **market** schema

**currently any stocks or bonds tables with non-alpha-numeric symbols have been inserted without those non-alpha-numeric symbols (e.g. GC=F becomes the table GCF ).
The exception to this rule is if a stockname has a dot '.' we represent it with an underscore '_' instead. (e.g. BRK.B becomes the table BRK_B)**

This code should be run in pgadmins query tool.

## Local File Structure Requirements

Any python Files run that use:
- csv files should have the subdirectory 'input' from where they are run with the csv's inside
- log files should have the subdirectory 'output' from where they are run (also necessary for sector retrieval and inserting)

rough example show below
```
├── input/
│   ├── A.csv
│   ├── AAPL.csv
│   ├── ...
│   └── ZTS.csv
└── output/
    ├── RawInsertLog.txt
    ├── ...
    └── SectorFixedList.csv
```
## Python scripts

Use cases along with specific requirements will be explained for the following python files here.

### SectorRetrievalToCSV.py

This script uses a specified list of stocks and queries the yfinance library to extract their sectors and replace any spaces ' ' with underscores '_'. The list you use must have dashes '-' in place of dots '.' if dots are present in the ticker symbol to query yfinance and should be casted back to dots after stored in the dataframe (currently hard-coded). Also as the stock symbol 'FI' has recently changed to 'FISV' you must use FI for the query and cast back to FISV in dataframe after (currently hard-coded).

sector data is then stored in SectorFixedList.csv found in the ./output directory

### DataInsertionFromCSV.py

This file takes all csv's from the ./input directory and tries to insert them into the database using the lowercase names of the files stripped of their file extension (e.g. AAPL.csv tries to insert into table aapl). 

A log file named RawInsertLog.txt is created in the ./output directory and contains data about each specific files attempt to be inserted into a table. 

The COPY command is used for efficiency as using regular INSERT commands are too slow for large chunks of data.

In this script, sectors are also inserted into the database from the SectorFixedList.csv found in the ./output directory that can be created by running the SectorRetrievalToCSV.py script. These are not logged.


### RawDataFormatterDBtoDB.py

This script takes a list of stocks (must match table names format described above) and transforms them into the current model features that will be used to train the model. This involves querying the raw tables for each stock in the fir database to transform and insert the data into the ModelFeatures table.

The COPY command is used for efficiency as using regular INSERT commands are too slow for large chunks of data.

Data Insertion should take around 9.5 minutes per 1,000,000 rows

This script may crash due to memory issues if running for a massive amount of data on a computer that cannot handle it. If you are attempting to do this just do a few stocks in the list at a time.

I will admit the logic of this file is currently a bit of a mess and should be improved later if time permits. Making a log file would be extremely useful for debugging.

### ModelDataUploadFromCSV.py

This script is only to be used if the database insertion failed using the RawDataFormatterDBtoDB.py script but you are sure the data is correctly formatted. This is because if the insertion fails the data will be backed up as ModelDatasetFormatTemp.csv in the output directory. 

Data Insertion should take around 9.5 minutes per 1,000,000 rows
