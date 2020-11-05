import requests
import json
import re
import time
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""

thedict = {}
tracking = {}
tracking['64.62.238.202'] = '64.62.238.2'
active = []
activeddos = []
datadict = {}
while True:
  data = requests.get(url, auth=(username, password)).content
  datadict = json.loads(data)
  try:
    ips = []
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
        #print("Not in active")
        active.append(i)
        print("DDOS HIT: "+str(i))
        if i not in activeddos:
          print("We set a active ddos for cgnat"+str(tracking[i]))
          tracking[i]
          activeddos.append(tracking[i])
    # lets check to see if a ddos is gone
    for i in active:
      #print("Active IP: "+i)
      if i not in ips:
        print("DDOS is gone: "+str(i))
        active.remove(i)
  except Exception as ex:
    pass
  time.sleep(1)