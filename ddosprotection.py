import requests
import json
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""
datadict = {}
data = requests.get(url, auth=(username, password)).content
json_object = json.load(data)
print(str(json_object[0]['values']))

#for i in datadict:
#  line = datadict[i]
#  print("Each: "+str(line))
#  for k in line:
#    print(str(k))
#    #if k == "name":
#    #  gname = datadict[i][k]