#!/bin/bash
rm /home/darkness4869/Documents/Corporate_Database_Builder/Logs/CDB.log
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
source /home/darkness4869/Documents/Corporate_Database_Builder/venv/bin/activate
python3 /home/darkness4869/Documents/Corporate_Database_Builder/Auto/collect_corporate_metadata.py
killall Xvfb
