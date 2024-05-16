import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import ignored.JiraKey as jiraKey

url = "https://midwesthoseit.atlassian.net/rest/api/3/search"

auth = HTTPBasicAuth("cstogsdill@midwesthose.com", jiraKey.apiKey)

headers = {
  "Accept": "application/json"
}


""" Query for the following locations:
ALI
BAK
BAT
CAS
DAL
DEN
DKN
DIL
ELR
LAK
FTW
GRE
HOB
HOU
LAF
KIL
ODE
OKC
OKW
POM
PAS
PIT
SAN
SLC
VER
WIL
COR
LAC
MWH
CHR
CALAX
"""
queries = {
    "DEN" : {'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = DEN'},
    "OKC" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" in (OKC, OKC-ACCT, OKC-CORP, OKC-CPIC, OKC-DIST, OKC-EXEC, OKC-HR, OKC-IT, OKC-MFG, OKC-SALES)'},
    "OKW" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = OKW'},
    "POM" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = POM'},
    "PAS" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = PAS'},
    "PIT" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = PIT'},
    "SAN" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = SAN'},
    "SLC" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = SLC'},
    "VER" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = VER'},
    "WIL" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = WIL'},
    "COR" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = COR'},
    "LAC" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = LAC'},
    "MWH" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = "COMPANY WIDE"'},
    "CHR" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = CHR'},
    "CALAX" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = CALAX'},
    "ALI" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = ALI'},
    "BAK" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = BAK'},
    "BAT" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = BAT'},
    "CAS" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = CAS'},
    "DAL" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = DAL'},
    "DKN" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = DKN'},
    "DIL" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = DIL'},
    "ELR" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = ELR'},
    "LAK" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = LAK'},
    "FTW" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = FTW'},
    "GRE" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = GRE'},
    "HOB" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = HOB'},
    "HOU" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = HOU'},
    "LAF" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = LAF'},
    "KIL" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = KIL'},
    "ODE" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = ODE'},
    "CHR" :{'jql': 'createdDate < endOfMonth(-1) and createdDate >= startOfMonth(-1) AND "Store Location" = CHR'},

}

# setup csv column headers
csv_columns = ['Location', 'Ticket Count']
csv_rows = []
csv_file = "TicketCountData.csv"

for location in queries:
    response = requests.request(
    "GET",
    url,
    headers=headers,
    params=queries[location],
    auth=auth
    )

    # responseJson = json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))
    responseJson = json.loads(response.text)
    print(f"{location} : {responseJson['total']}")
    csv_rows.append({'Location': location, 'Ticket Count': responseJson['total']})

# export to csv file

with open(csv_file, 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for row in csv_rows:
        writer.writerow(row)

