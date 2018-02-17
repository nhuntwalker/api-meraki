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

with open(os.path.join(os.pardir, 'api/') + 'api_network_ids.csv', mode='r') as networkid:
    reader = csv.reader(networkid)
    next(reader, None)  # Skips the row containing headers
    for row in reader:
        print(row[0])

        # PUT - Customize the URL and payload based on the query. Verify the variable order MATCHES the API documentation
        query = requests.put(baseUrl+ '/networks/'+row[0],
                         headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'}, data=row)
                         # I recommend using POSTMAN for crafting queries:   https://www.getpostman.com

        #  View API response
        print(query.status_code)

        # Dump output to JSON file with pretty (indented) printing for readability
        with open(os.path.join(os.pardir, 'data/')+row[0]+'_output.json', "w") as output:
                answer = query.json()
                json.dump(answer, output, indent=4)