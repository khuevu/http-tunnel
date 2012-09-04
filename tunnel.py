#!/usr/bin/env python
import socket
import httplib, urllib
from uuid import uuid4

HOST = ''
PORT = 50067

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

remote_url = 'localhost'
remote_port = 8888

target_url = 'www.google.com'
target_port = 80

#generate connection id 
c_id = uuid4()
remote_conn = httplib.HTTPConnection(remote_url, remote_port)
#send request for tunneling
params = urllib.urlencode({"@host": target_url, "@port": target_port})
headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
remote_conn.request("POST", "/" + c_id, params, headers)
response = conn.getresponse()

#create a loop to read and write data
while True: 
    #read data
    remote_conn.request("GET", "/" + c_id)
    read_res = conn.getresponse()
    if read_res.status != 200:
        break
    data = read_res.read()
    print data
    conn.sendall(data)
     
    #Write data 
    write_data = s.recv(1024) 
    if not write_data:
        break
    params = urllib.urlencode({"@data": write_data})
    remote_conn.request("PUT", "/" + c_id, params, headers)  
    write_res = remote_conn.getresponse()
    print write_res.status 

