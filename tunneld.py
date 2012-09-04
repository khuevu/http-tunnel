#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer 
import socket

class ProxyRequestHandler(BaseHTTPRequestHandler):
    sockets = {}
    MAX_BUFFER = 1024 * 128

    def _get_connection_id(self):
        return self.path.split('/')[-1]

    def _get_socket(self):
        id = self._get_connection_id()
        return self.sockets[id] 

    def _close_socket(self):
        id = self._get_connection_id()
        s = self.sockets[id]
        if s:
            s.close()

    def do_GET(self):
        """Read data from RemoteAddr and return to client through http response
        """
        s = self._get_socket()
        if s:
            remote_data = s.recv(self.MAX_BUFFER)
            self.send_response(200)
            self.wfile.write(remote_data)

    def do_POST(self):
        """Create TCP Connection with the RemoteAddr
        """
        id = self._get_connection_id() 
        req_data = self.rfile.read()
        print req_data
        (remote_host, remote_port) = req_data.split(':')
        remote_port = int(remote_port)
        #open socket connection to remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((remote_host, remote_port))
        print 'open connection to remote server'
        self.sockets[id] = s

    def do_PUT(self):
        """Read data from HTTP Request and send over TcpConnection to RemoteAddr
        """
        id = self._get_connection_id()
        s = self.sockets[id]
        send_data = self.rfile.read() 
        s.sendall(send_data)
        

    def do_DELETE(self): 
        self._close_socket()

def run_server(server_class=HTTPServer, handler_class=ProxyRequestHandler): 
    server_address = ('', 8888)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
