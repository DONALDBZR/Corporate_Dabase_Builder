#!/bin/bash
mkdir ./Cache
mkdir ./Cache/CorporateDataCollection
mkdir ./Cache/CorporateDocumentFile
mkdir ./Cache/CorporateDocumentFile/Documents
mkdir ./Cache/CorporateDocumentFile/Metadata
cd /home/darkness4869/Documents/Corporate_Database_Builder/
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
deactivate
