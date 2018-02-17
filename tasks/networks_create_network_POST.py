import json,csv
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

        with open(os.path.join(os.pardir, 'data/') +'createNetwork.csv', "r") as networks:
            reader = csv.reader(networks)
            next(reader, None)  # Skips the row containing headers
            for row in reader:
                name = row[1]
                tags = row[3]
                nettype = row[4]
                tz = row[2]


                # PUT - Update an administrator
                meraki.addnetwork(apikey,orgid,name,nettype=nettype,tags=tags,tz=tz)
if __name__ == '__main__':
    main()