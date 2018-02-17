import json, csv
import os, requests

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    # Defines the root Organization id for the networks in question
    orgid = keys[0]["orgid"]
    with open(os.path.join(os.pardir, "data/")+"clients_policy_report.csv", "r") as devices:
        reader = csv.reader(devices)
        next(reader, None)  # Skips the row containing headers
        for row in reader:
            mac = row[5]
            id = row[1]
            # GET - List the dashboard administrators in this organization
            query = requests.get('https://api.meraki.com/api/v0'+'/networks'+id+'/clients/'+mac+'/splashAuthorizationStatus',
                                 headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})

            with open(os.path.join(os.pardir, 'data/')+orgid+'_clients_splash_auth.json', "w") as f:
                    answer = query.json()
                    json.dump(answer, f, indent=4)