import requests
import json
import re
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""
datadict = {}
thedict = {}
ips = []
active = []
data = requests.get(url, auth=(username, password)).content
datadict = json.loads(data)
thedict = datadict['values']
for i in thedict:
  #print(i)
  for e in i:
    #print(i[e])
    #print(e)
    ip = i[e]
    m = re.search(r"(\d+\.\d+\.\d+\.\d+)\/\d+", ip)
    if m:
      ip = m.group(1)
    key = e
    if e == "ip":
      ips.append(ip)
 

for i in ips:
  print("IP: "+i)
  for ii in active:
    if not i == ii:
      print("We do not have it yet")