import json, csv
import os, requests

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    # Defines the root Organization id for the networks in question
    orgid = keys[0]["orgid"]

    with open(os.path.join(os.pardir, 'api/') + 'api_network_ids.csv', "r") as networks:
        reader = csv.reader(networks)
        next(reader, None)  # Skips the row containing headers
        for row in reader:
            networkid = row[0]

            # GET - List the access policies for this network. Only valid for MS networks.
            query = requests.get('https://api.meraki.com/api/v0/networks/' + "N_000000000000000" + '/accessPolicies',
                                headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})


            with open(os.path.join(os.pardir, 'data/')+networkid+'_traffic.json', "w") as f:
                    answer = query.json()
                    json.dump(answer, f, indent=4)