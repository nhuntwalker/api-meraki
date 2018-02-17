import requests, csv, json, os


with open(os.path.join(os.pardir,"api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    #Defines the root Organization id for the networks in question
    orgid = keys[0]["orgid"]

# GET request to Meraki API for list of network ID's
query = requests.get('https://api.meraki.com/api/v0/organizations/'+orgid+'/configTemplates',
                 headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})

with open('api_network_ids.csv', "w") as csvfile:
    answer = query.json()
    output = csv.writer(csvfile) #create a csv.write
    output.writerow(answer[0].keys())  # header row
    for row in answer:
        output.writerow(row.values()) #values row