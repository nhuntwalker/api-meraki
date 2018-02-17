import requests,os,json

# Use this template for creating custom GET requests for any API.

# Defines the plain text API key generated in your platforms dashboard
apiKey = ""

# enter the base URL for your API call
baseUrl = "https://api.meraki.com/api/v0/"
id = ""
mac = ""
payload = [{
  "ssids": {
    "0": {
      "isAuthorized": True,
      "authorizedAt": "2017-07-19 16:24:13 UTC",
      "expiresAt": "2017-07-20 16:24:13 UTC"
    },
    "2": {
      "isAuthorized": False
    }
  }
}]

# PUT - Customize the URL and payload based on the query. Verify the variable order MATCHES the API documentation
query = requests.put(baseUrl+'/networks'+id+'/clients/'+mac+'/splashAuthorizationStatus',
                     headers={'X-Cisco-Meraki-API-Key': apiKey, 'Content-Type': 'application/json'}, data=payload)
                     # I recommend using POSTMAN for crafting queries:   https://www.getpostman.com

#  View API response
print(query.status_code)
