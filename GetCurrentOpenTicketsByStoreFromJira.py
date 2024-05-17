import requests
from requests.auth import HTTPBasicAuth
import json
import csv
import ignored.JiraKey as jiraKey

# setup csv info
csv_columns = ['Location', 'Ticket Count']
csv_rows = []
csv_file = "TotalTicketsPerStore.csv"

url = "https://midwesthoseit.atlassian.net/rest/api/3/search"

auth = HTTPBasicAuth("cstogsdill@midwesthose.com", jiraKey.apiKey)

headers = {
  "Accept": "application/json"
}


queries = {
    "ALI" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = ALI'},
    "BAK" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = BAK'},
    "BAT" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = BAT'},
    "CAS" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = CAS'},
    "DAL" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = DAL'},
    "DEN" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = DEN'},
    "DKN" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = DKN'},
    "DIL" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = DIL'},
    "ELR" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = ELR'},
    "LAK" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = LAK'},
    "FTW" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = FTW'},
    "GRE" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = GRE'},
    "HOB" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = HOB'},
    "HOU" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = HOU'},
    "LAF" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = LAF'},
    "KIL" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = KIL'},
    "ODE" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = ODE'},
    "OKC" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" in (OKC, OKC-ACCT, OKC-CORP, OKC-CPIC, OKC-DIST, OKC-EXEC, OKC-HR, OKC-IT, OKC-MFG, OKC-SALES)'},
    "OKW" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = OKW'},
    "POM" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = POM'},
    "PAS" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = PAS'},
    "PIT" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = PIT'},
    "SAN" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = SAN'},
    "SLC" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = SLC'},
    "VER" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = VER'},
    "WIL" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = WIL'},
    "COR" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = COR'},
    "LAC" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = LAC'},
    "MWH" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = "COMPANY WIDE"'},
    "CHR" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = CHR'},
    "CALAX" : {'jql': 'status NOT IN ("Resolved", "Closed", "Canceled", "DONE")  AND "Store Location" = CALAX'}    
}



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