#!/usr/bin/env python
import socket
import httplib, urllib
from uuid import uuid4
import time

"""Local port the program will listen to 
"""
HOST = ''
PORT = 50065

"""Remote address to http tunnel to
"""
remote_url = 'localhost'
remote_port = 8888

"""Target Address
"""
target_url = 'chat.freenode.net'
target_port = 8001

#generate unique connection ID
c_id = uuid4()
print 'creating tunnel connection with id %s' % str(c_id)
http_conn = httplib.HTTPConnection(remote_url, remote_port)
#send request for tunneling
params = urllib.urlencode({"host": target_url, "port": target_port})
headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
http_conn.request("POST", "/" + str(c_id), params, headers)
response = http_conn.getresponse()
print 'Created connection with status %d ' % response.status

#listen for connection
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print 'Connected by', addr

#create a loop to read and write data
MAX_BUFFER = 1024 * 640
while True: 
    #read data from socket and tunnel to target add. through http connection
    write_data = conn.recv(MAX_BUFFER) 
    print write_data
    if not write_data:
        time.sleep(2)  
        print 'Waiting for coming traffic'
        continue
    params = urllib.urlencode({"data": write_data})
    try:
        http_conn.request("PUT", "/" + str(c_id), params, headers)  
        write_res = http_conn.getresponse()
        print write_res.status 
    except httplib.HTTPException, e:
        print 'HTTPException - %s' % e.reason
        #close remote connection
        http_conn.request("DELETE", "/" + str(c_id))
        http_conn.getresponse()

    #Retrieve data from HTTP connection and write to the listen socket 
    http_conn.request("GET", "/" + str(c_id))
    read_res = http_conn.getresponse()
    if read_res.status != 200:
        break
    read_data = read_res.read()
    conn.sendall(read_data)
     
    
