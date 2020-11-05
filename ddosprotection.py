import requests
import json
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""
datadict = {}
data = requests.get(url, auth=(username, password)).content
output_json = json.loads(data)
for i in output_json['values']:
  print(i)
  for k in output_json[i]:
          print(k)