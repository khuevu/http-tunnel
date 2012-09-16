import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 8889))

commands = ["CAP LS", "NICK abc", "USER abc abc irc.freenode.net :abc", "CAP REQ :identify-msg", "CAP END", "NOTICE frigg :.VERSION xchat 2.8.8 Ubuntu"]

order = 0
s.sendall("NICK abcxyz\r\n")
s.sendall("USER abcxyz abcxyz irc.freenode.net :abcxyz\r\n")
while True:
    data = s.recv(1024)
    print data
    
#import httplib, urllib
#conn = httplib.HTTPConnection('localhost', 8889)
#conn.request("GET", "http://www.google.com")
#response = conn.getresponse()
#print response.status, response.reason
#print response.read()
    
