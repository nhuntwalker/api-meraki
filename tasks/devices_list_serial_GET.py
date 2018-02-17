import json,csv
import os, requests

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    with open(os.path.join(os.pardir, 'api/') + 'api_network_ids.csv', mode='r') as networkid:
        reader = csv.reader(networkid)
        next(reader, None)  # Skips the row containing headers
        for row in reader:
            query = requests.get('https://api.meraki.com/api/v0/networks/'+row[0]+'/devices',
                                 headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})

            with open(os.path.join(os.pardir, 'data/') +row[0]+ '_devices_serial.json', "w") as f:
                answer = query.json()
                json.dump(answer, f, indent=4)