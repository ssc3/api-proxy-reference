import requests
import json

# In docker
lHeaders = {"content-type": "application/json"}
url="http://127.0.0.1:8001/v1/devices"
r = requests.get(url, verify=False, stream=True)
print (r.text)

# On ubuntu localhost
'''lHeaders = {"content-type": "application/json"}
url="http://127.0.0.1:5000/v1/devices"
r = requests.get(url, verify=False, stream=True)
print (r.text)
'''
