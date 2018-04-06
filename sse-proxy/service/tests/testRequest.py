import requests
import json


testConfigJson = json.load(open('testConfig.json'))
deviceId = testConfigJson['deviceId']

lHeaders = {"content-type": "application/json"}
url="http://127.0.0.1:5000/v1/device/" + deviceId + "/api/node/class/fvTenant.json"
r = requests.get(url, verify=False, stream=True)
print (r.text)