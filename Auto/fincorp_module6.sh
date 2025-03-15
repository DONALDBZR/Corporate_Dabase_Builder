#!/bin/bash
rm /home/darkness4869/Documents/Corporate_Database_Builder/Logs/CDB.log
source /home/darkness4869/Documents/Corporate_Database_Builder/venv/bin/activate
python3 /home/darkness4869/Documents/Corporate_Database_Builder/Auto/curate_office_bearers.py
deactivate
