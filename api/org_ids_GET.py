from meraki import meraki
import json, os

with open(os.path.join(os.pardir,"api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    orgids = meraki.myorgaccess(apikey)
    print(orgids)

    with open("api_org_ids.json", 'w', ) as f:
        json.dump(orgids, f, indent=4)