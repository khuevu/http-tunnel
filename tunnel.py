#!/usr/bin/env python
import socket
import httplib, urllib
from uuid import uuid4

HOST = ''
PORT = 50067


remote_url = 'localhost'
remote_port = 8888

target_url = 'www.google.com'
target_port = 80

#generate connection id 
c_id = uuid4()
print 'creating tunnel connection with id %s' % str(c_id)
remote_conn = httplib.HTTPConnection(remote_url, remote_port)
#send request for tunneling
params = urllib.urlencode({"host": target_url, "port": target_port})
headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
print 'making request to create connection'
remote_conn.request("POST", "/" + str(c_id), params, headers)
response = remote_conn.getresponse()
print 'Get here ? '
print response.status

#listen for connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

#create a loop to read and write data
while True: 
    #read data from socket and tunnel to target add. through http connection
    remote_conn.request("GET", "/" + str(c_id))
    read_res = conn.getresponse()
    if read_res.status != 200:
        break
    data = read_res.read()
    print data
    conn.sendall(data)
     
    #Retrieve data from HTTP connection and write to the listen socket 
    write_data = s.recv(1024) 
    print write_data
    if not write_data:
        break
    params = urllib.urlencode({"@data": write_data})
    remote_conn.request("PUT", "/" + c_id, params, headers)  
    write_res = remote_conn.getresponse()
    print write_res.status 

