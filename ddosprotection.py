import requests
url = 'https://updates.opendns.com/nic/update?hostname='
username = 'username'
password = 'password'
print(requests.get(url, auth=(username, password)).content)