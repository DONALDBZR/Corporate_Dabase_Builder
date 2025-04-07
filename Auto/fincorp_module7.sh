#!/bin/bash
cd /home/darkness4869/Documents/Corporate_Database_Builder/
rm /home/darkness4869/Documents/Corporate_Database_Builder/Logs/CDB.log
source /home/darkness4869/Documents/Corporate_Database_Builder/venv/bin/activate
python3 /home/darkness4869/Documents/Corporate_Database_Builder/Auto/curate_shareholders.py
deactivate
