import urllib
with urllib.request.urlopen('http://python.org/') as response:
   html = response.read()