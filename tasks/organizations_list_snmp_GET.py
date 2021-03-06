import json, csv
import os, requests

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    # Defines the root Organization id for the networks in question
    orgid = keys[0]["id"]

    # GET - List the vlans for this network
    query = requests.get('https://api.meraki.com/api/v0/organizations/' + orgid + '/snmp',
                         headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})
    print(query.status_code)

    with open(os.path.join(os.pardir, 'data/')+orgid+'_snmp.json', "w") as f:
            answer = query.json()
            json.dump(answer, f, indent=4)

