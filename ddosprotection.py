import requests
import json
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""
datadict = {}
thedict = {}
data = requests.get(url, auth=(username, password)).content
datadict = json.loads(data)
thedict = datadict['values']
for i in thedict:
  for e in i:
    print(e['ip'])