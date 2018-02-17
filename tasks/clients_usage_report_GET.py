import json, csv
import os, requests

with open(os.path.join(os.pardir, "api/api_credentials.json"), "r") as creds:
    # Reads the api_credentials.json file for authentication
    keys = json.load(creds)

    # Defines the plain text API key generated in the Meraki portal
    apikey = keys[0]["apikey"]

    with open(os.path.join(os.pardir, "data/")+"devices_serial.json", "r") as devices:
        payload = json.load(devices)
        for data in payload:
            serial = data["serial"]
            name = data["name"]
            timespan= "86400" #24hrs=86400, 1week=604800, 30days = 864000
            """GET - List the clients of a device, up to a maximum of a month ago. The usage of each client is returned in kilobytes. 
             If the device is a switch, the switchport is returned; otherwise the switchport field is null. """

            query = requests.get('https://api.meraki.com/api/v0/devices/'+serial+'/clients?timespan='+timespan,
                                 headers={'X-Cisco-Meraki-API-Key': apikey, 'Content-Type': 'application/json'})

            # Uncomment for JSON output
           # with open(os.path.join(os.pardir, 'data/')+name+'_clients.json', "w") as f:
           #         answer = query.json()
            #        json.dump(answer, f, indent=4)

            with open(os.path.join(os.pardir, 'data/')+name+'_clients.csv', "w") as csvfile:
                answer = query.json()
                output = csv.writer(csvfile)  # create a csv.write
                output.writerow(answer[0].keys())  # header row
                for row in answer:
                    output.writerow(row.values())  # values row