# This bash script is intended to simply enviornment setup for the Data Collector 

# Note: env.sh needs to be filled in correctly, see readme file 

set -e  # Exit immediately on error

# Ensure Python and pip are installed (venv module is included)
sudo dnf install -y python3 python3-pip

# Remove any old virtual environment
rm -rf ~/envs/market

# Create a new venv using system Python
python3 -m venv ~/envs/market

# Activate it
source ~/envs/market/bin/activate

# Upgrade pip installer
python -m pip install --upgrade pip setuptools wheel

# Install required Python packages
pip install requests python-dateutil pytz psycopg2-binary

echo "Virtual environment ready at ~/envs/market"
echo "Run 'source ~/envs/market/bin/activate' before running your collector."






