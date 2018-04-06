import requests
import json


lHeaders = {"content-type": "application/json"}
url="http://127.0.0.1:80/v1/devices"
r = requests.get(url, verify=False, stream=True)
print (r.text)

