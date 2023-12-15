#!/bin/bash


# Script Logic Description:
# 1) Login to Azure with the Service Principal and do IP Whitelisting for MSSQL
# 2) Run the EbayListingsRetrieval script to get the active Ebay listings
# 3) Run the EbayListingsUpload script to update the active Ebay listings to the database
# 4) Run the EbayListingsDiff script to get the diff between the desired state and the current state
# 5) Run the EbayListingsPatch script to apply all the diffs to get to the desired state (C/U/D)
# 6?) possibly send out a notification or something, or enter a new row in a special
#     table that would be more like a signing sheet, with each entry representing an 
#     instance that ran, letting us know the date/time it ran, whether or not it made 
#     any changes, and possibly also a list of changes applied

# Step #1: Login to Azure with the Service Principal and do IP Whitelisting for MSSQL

CLIENT_ID="---"
CLIENT_SECRET="---"
TENANT_ID="---"
SQL_SERVER_NAME="testing-trulinx"
RESOURCE_GROUP="aztomwh"

public_ip=$(curl -s ifconfig.me)

az login --service-principal -u $CLIENT_ID -p $CLIENT_SECRET --tenant $TENANT_ID
az sql server firewall-rule create -g $RESOURCE_GROUP -s $SQL_SERVER_NAME -n AllowEbayScriptIP --start-ip-address $public_ip --end-ip-address $public_ip

pip install -r requirements.txt

# Step #2: Run the EbayListingsRetrieval script to get the active Ebay listings

# Generate `ebay-listings.json` with data from the Ebay API
python EbayListingsRetrieval.py

# Step #3: Run the EbayListingsUpload script to upload the active Ebay listings to the database

# Upload `ebay-listings.json` content to the Shadow DB in the EbayItems table
python EbayListingsUpload.py

# Step #4: Run the EbayListingsDiff script to get the diff between the desired state and the current state

python EbayListingsDiff.py

# Step #5: Run the EbayListingsPatch script to apply all the diffs to get to the desired state (C/U/D)

python EbayListingsPatch.py

# Step #6: possibly send out a notification or something

python EbayListingsNotification.py