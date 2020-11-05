import requests
import json
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""
datadict = {}
thedict = {}
ips = []
data = requests.get(url, auth=(username, password)).content
datadict = json.loads(data)
thedict = datadict['values']
for i in thedict:
  #print(i)
  for e in i:
    #print(i[e])
    #print(e)
    ip = i[e]
    key = e
    if e == "ip":
      ips.append(ip)
 

for i in ips:
  print("IP: "+i)