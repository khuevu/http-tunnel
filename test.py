import httplib, urllib
conn = httplib.HTTPConnection('localhost', 50065)
conn.request("GET", "http://www.google.com")
response = conn.getresponse()
print response.status, response.reason
print response.read()
