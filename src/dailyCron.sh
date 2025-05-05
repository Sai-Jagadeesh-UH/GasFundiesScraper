#!/bin/bash

# === CONFIGURATION ===
APP_DIR="/home/gfdev/App"           # Path to your App folder
VENV_PATH="$APP_DIR/venv"             # Virtual environment directory
PYTHON_SCRIPT="$APP_DIR/GasFundiesScraper/src/playwrightscraper/dailyScrape.py"      # Python script to run
LOG_FILE="$APP_DIR/GasFundiesScraper/src/playwrightscraper/logs/CRONLOG_$(date +%b).txt"      # Output log file

# === SCRIPT EXECUTION ===
echo "Starting CRON for $(date)" >> "$LOG_FILE"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Run the Python script
python "$PYTHON_SCRIPT"


echo "CRON run complete  $(date)" >> "$LOG_FILE"