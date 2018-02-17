import json, csv
import os, requests

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    networkid = "N_655273745782434536"
    name = networkid
    with open(os.path.join(os.pardir, "data/")+"22F-AP10_clients.csv", "r") as devices:
        reader = csv.reader(devices)
        next(reader, None)  # Skips the row containing headers
        for row in reader:
            mac = row[5]
            timespan= "2000" #24hrs=86400, 1week=604800, 30days = 864000

            # GET - Return the policy assigned to a client on the network.
            query = requests.get('https://api.meraki.com/api/v0/networks/'+networkid+'/clients/'+mac+'/policy?timespan='+timespan,
                                 headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})

            # Uncomment for JSON output
            with open(os.path.join(os.pardir, 'data/')+name+'_clients_policy_report.json', "w") as f:
                    answer = query.json()
                    print(answer)
                    json.dump(answer, f, indent=4)