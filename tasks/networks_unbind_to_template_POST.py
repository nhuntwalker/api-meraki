import requests,os,json, csv

# Defines the plain text API key generated in your platforms dashboard
with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    # Defines the root Organization id for the networks in question
    orgid = keys[0]["orgid"]

    # enter the base URL for your API call
    baseUrl = "https://api.meraki.com/api/v0/"

    # Enter the NetID of the config template you want to bind to
    configTemplate = ""

    with open(os.path.join(os.pardir, 'data/') + 'bind_network_ids.csv', mode='r') as networkid:
        reader = csv.reader(networkid)
        next(reader, None)  # Skips the row containing headers
        for row in reader:
            print(row[0])

            # PUT - Customize the URL and payload based on the query. Verify the variable order MATCHES the API documentation
            query = requests.post(baseUrl + '/networks/' + row[0]+"/unbind",
                                 headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'},
                                 data={"configTemplateId":configTemplate, "autoBind":False})

            #  View API response
            print(query.status_code)