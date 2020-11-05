import requests
url = 'http://127.0.0.1:10007/license'
username = 'admin'
password = '3110'
print(requests.get(url, auth=(username, password)).content)