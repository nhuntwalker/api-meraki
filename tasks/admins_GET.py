import json
import os, requests

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    # Defines the root Organization id for the networks in question
    orgid = keys[0]["orgid"]

    # GET - List the dashboard administrators in this organization
    query = requests.get('https://api.meraki.com/api/v0/organizations/' + orgid + '/admins',
                         headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})

    with open(os.path.join(os.pardir, 'data/')+orgid+'_admins.json', "w") as f:
            answer = query.json()
            json.dump(answer, f, indent=4)