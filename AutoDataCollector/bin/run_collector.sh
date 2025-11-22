#!/bin/bash
# This bash script is intended to simplify the execution of Data Collector 

# Activate Python virtual environment
source ~/envs/market/bin/activate

# Load environment variables (database connection, API keys, etc.)
source /home/$USER/AlgorithmicTrading/AutoDataCollector/env.sh

# Run the data collector script
python /home/$USER/AlgorithmicTrading/AutoDataCollector/bin/data_collector.py



