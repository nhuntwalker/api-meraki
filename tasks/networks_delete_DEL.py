import json, csv
import os
from meraki import meraki
def main():

    with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
        # Reads the api_credentials.json file for authentication
        keys = json.load(creds)

        # Defines the plain text API key generated in the Meraki portal
        apikey = keys[0]["apikey"]

        # Defines the root Organization id for the networks in question
        orgid = keys[0]["orgid"]

    with open(os.path.join(os.pardir, "data/") + "delete_network_ids.csv", "r") as devices:
        reader = csv.reader(devices)
        next(reader, None)  # Skips the row containing headers
        for row in reader:
            networkid = row[0]
            print(networkid)

            # DEL - Revoke all access for a dashboard administrator within this organization
            meraki.delnetwork(apikey,networkid)

if __name__ == '__main__':
    main()