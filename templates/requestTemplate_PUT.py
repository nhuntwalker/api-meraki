import requests,os,json

# Use this template for creating custom GET requests for any API.

# Defines the plain text API key generated in your platforms dashboard
apiKey = ""

# enter the base URL for your API call
baseUrl = "https://api.meraki.com/api/v0/"
id = ""
mac = ""
payload = []

# PUT - Customize the URL and payload based on the query. Verify the variable order MATCHES the API documentation
query = requests.put(baseUrl+ 'ExampleCall',
                     headers={'X-Cisco-Meraki-API-Key': apiKey, 'Content-Type': 'application/json'}, data=payload)
                     # I recommend using POSTMAN for crafting queries:   https://www.getpostman.com

#  View API response
print(query.status_code)

# Dump output to JSON file with pretty (indented) printing for readability
with open(os.path.join(os.pardir, 'data/')+'_output.json', "w") as output:
        answer = query.json()
        json.dump(answer, output, indent=4)