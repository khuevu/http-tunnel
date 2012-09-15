#!/usr/bin/env python
import socket
import httplib, urllib
from uuid import uuid4
import time
import threading
import argparse

BUFFER = 1024 * 50

#set global timeout
socket.setdefaulttimeout(5)

class Connection():

    def __init__(self, connection_id, remote_addr):
        self.id = connection_id
        self.http_conn = httplib.HTTPConnection(remote_addr['host'], remote_addr['port'])

    def create(self, target_addr):
        params = urllib.urlencode({"host": target_addr['host'], "port": target_addr['port']})
        headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        self.http_conn.request("POST", "/" + self.id, params, headers)

        response = self.http_conn.getresponse()
        if response.status == 200:
            print 'Successfully create connection'
            return True 
        else:
            print 'Fail to establish connection: status %s because %s' % (response.status, response.reason)
            return False 

    def send(self, data):
        params = urllib.urlencode({"data": data})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try: 
            self.http_conn.request("PUT", "/" + self.id, params, headers)  
            response = self.http_conn.getresponse()
            print response.status 
        except (httplib.HTTPResponse, socket.error) as ex:
            print "Error Sending Data: %s" % ex

    def receive(self):
        try: 
            self.http_conn.request("GET", "/" + self.id)
            response = self.http_conn.getresponse()
            if response.status == 200:
                data = response.read()
                return data
            else: 
                print "GET HTTP Status: %d" % response.status
                return ""
        except (httplib.HTTPResponse, socket.error) as ex:
            print "Error Receiving Data: %s" % ex
            return "" 

    def close(self):
        self.http_conn.request("DELETE", "/" + self.id)
        self.http_conn.getresponse()

class SendThread(threading.Thread):

    """
    Thread to send data to remote host
    """
    
    def __init__(self, socket, conn):
        threading.Thread.__init__(self, name="Send-Thread")
        self.socket = socket
        self.conn = conn

    def run(self):
        while True:
            data = self.socket.recv(BUFFER)
            print 'Send data', data
            self.conn.send(data)

class ReceiveThread(threading.Thread):

    """
    Thread to receive data from remote host
    """

    def __init__(self, socket, conn):
        threading.Thread.__init__(self, name="Receive-Thread")
        self.socket = socket
        self.conn = conn

    def run(self):
        while True:
            data = self.conn.receive()
            print 'Receive data', data
            self.socket.sendall(data)

class ClientWorker(threading.Thread):

    def __init__(self, socket, remote_addr, target_addr):
        threading.Thread.__init__(self)
        self.socket = socket
        self.remote_addr = remote_addr 
        self.target_addr = target_addr

    def run(self):
        #generate unique connection ID
        connection_id = str(uuid4())
        connection = Connection(connection_id, self.remote_addr)

        if connection.create(self.target_addr):
            sender = SendThread(self.socket, Connection(connection_id, self.remote_addr))
            receiver = ReceiveThread(self.socket, Connection(connection_id, self.remote_addr))
            sender.start()
            receiver.start()


def start_tunnel(listen_port, remote_addr, target_addr):
    """Start tunnel"""
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.settimeout(None)
    listen_sock.bind(('', listen_port))
    listen_sock.listen(1)
    print "waiting for connection"
    while True:
        c_sock, addr = listen_sock.accept() 
        print "connected by ", addr
        worker = ClientWorker(c_sock, remote_addr, target_addr)
        worker.start()


if __name__ == "__main__":
    """Parse argument from command line and start tunnel"""

    parser = argparse.ArgumentParser(description='Start Tunnel')
    parser.add_argument('-p', default=8889, dest='listen_port', help='Port the tunnel listens to, (default to 8889)')
    parser.add_argument('target', metavar='Target Address', help='Specify the host and port of the target address in format Host:Port')
    parser.add_argument('-r', default='localhost:9999', dest='remote', help='Specify the host and port of the remote server to tunnel to (Default to localhost:9999)')

    args = parser.parse_args()

    target_addr = {"host": args.target.split(":")[0], "port": args.target.split(":")[1]}
    remote_addr = {"host": args.remote.split(":")[0], "port": args.remote.split(":")[1]}
    start_tunnel(args.listen_port, remote_addr, target_addr)



            
#"""Local port the program will listen to 
#"""
#HOST = ''
#PORT = 50065

#"""Remote address to http tunnel to
#"""
#remote_url = 'localhost'
#remote_port = 8888

#"""Target Address
#"""
#target_url = 'chat.freenode.net'
#target_port = 8001

##generate unique connection ID
#c_id = uuid4()
#print 'creating tunnel connection with id %s' % str(c_id)
#http_conn = httplib.HTTPConnection(remote_url, remote_port)
##send request for tunneling
#params = urllib.urlencode({"host": target_url, "port": target_port})
#headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#http_conn.request("POST", "/" + str(c_id), params, headers)
#response = http_conn.getresponse()
#print 'Created connection with status %d ' % response.status

##listen for connection
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.bind((HOST, PORT))
#s.listen(1)
#conn, addr = s.accept()
#print 'Connected by', addr

##create a loop to read and write data
#MAX_BUFFER = 1024 * 640
#while True: 
    ##read data from socket and tunnel to target add. through http connection
    #write_data = conn.recv(MAX_BUFFER) 
    #print write_data
    #if not write_data:
        #time.sleep(2)  
        #print 'Waiting for coming traffic'
        #continue
    #params = urllib.urlencode({"data": write_data})
    #try:
        #http_conn.request("PUT", "/" + str(c_id), params, headers)  
        #write_res = http_conn.getresponse()
        #print write_res.status 
    #except httplib.HTTPException, e:
        #print 'HTTPException - %s' % e.reason
        ##close remote connection
        #http_conn.request("DELETE", "/" + str(c_id))
        #http_conn.getresponse()

    ##Retrieve data from HTTP connection and write to the listen socket 
    #http_conn.request("GET", "/" + str(c_id))
    #read_res = http_conn.getresponse()
    #if read_res.status != 200:
        #break
    #read_data = read_res.read()
    #conn.sendall(read_data)
     
    
