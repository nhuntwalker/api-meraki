import json
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

    with open(os.path.join(os.pardir, "data/create_admins.json"), "r") as admins:
            access = json.load(admins)
            for admin in access["admins"]:
                name = admin["name"]
                email = admin["email"]
                orgaccess = admin["orgAccess"]
                print(name, email, orgaccess)

                # POST - Create a new dashboard administrator
                meraki.addadmin(apikey, orgid, email, name, orgaccess=orgaccess, tags=None, tagaccess=None, networks=None)

if __name__ == '__main__':
    main()