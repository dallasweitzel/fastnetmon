import requests
url = 'http://157.245.130.37:10007/license'
username = 'admin'
password = '3110'
print(requests.get(url, auth=(username, password)).content)