import requests,os,json

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    # Defines the root Organization id for the networks in question
    orgid = keys[0]["orgid"]

# enter the base URL for your API call
baseUrl = "https://dashboard.meraki.com/api/v0"

# GET - Customize the URL and payload based on the query. Verify the variable order MATCHES the API documentation
query = requests.get(baseUrl+'/organizations/'+orgid+'/configTemplates',
                     headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})
                     # I recommend using POSTMAN for crafting queries:   https://www.getpostman.com

# View API response
print(query.status_code)

# Dump output to JSON file with pretty (indented) printing for readability
with open(os.path.join(os.pardir, 'data/')+orgid+'configTemplates.json', "w") as output:
        answer = query.json()
        json.dump(answer, output, indent=4)