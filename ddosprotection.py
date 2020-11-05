import requests
import json
import re
import time
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""

thedict = {}
ips = []
active = []
datadict = {}
while True:
  data = requests.get(url, auth=(username, password)).content
  datadict = json.loads(data)
  if len(datadict['values']) > 0:
    thedict = datadict['values']
    # making list
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
 
    # looking for new ddos
    for i in ips:
      #print("IP: "+i)
      if i not in active:
        print("Not in active")
        active.append(i)


    # lets check to see if a ddos is gone
    for i in active:
      #print("Active IP: "+i)
      if i not in ips:
        print("Not longer in IPS")
        active.remove(i)

  time.sleep(1)