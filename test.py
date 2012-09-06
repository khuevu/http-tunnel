import httplib, urllib
conn = httplib.HTTPConnection('localhost', 50067)
conn.request("GET", "/")
response = conn.getresponse()
print response.status
