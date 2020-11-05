import requests
import json
url = 'http://157.245.130.37:10007/blackhole'
username = 'admin'
password = '3110'
data = ""
datadict = {}
data = requests.get(url, auth=(username, password)).content
blackholed_hosts = json.loads(data)

blackholed_ip_addresses = []
for blackholed_entity in blackholed_hosts.json()['values']:
    blackholed_ip = blackholed_entity['ip'].replace('/32', '', -1)
    blackholed_ip_addresses.append(blackholed_ip)