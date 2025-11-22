#!/bin/bash
# Bash script to simplify steps to run coverage test

# Activate Python virtual environment
source ~/envs/market/bin/activate

# Load environment variables (DB credentials, etc.)
source /home/$USER/AlgorithmicTrading/AutoDataCollector/env.sh

# Run the coverage test script
python /home/$USER/AlgorithmicTrading/AutoDataCollector/bin/coverage_test.py
