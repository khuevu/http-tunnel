#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer 
import socket
import cgi

class ProxyRequestHandler(BaseHTTPRequestHandler):
    """sockets: contains all sockets connecting to target address for each connection from client
    """
    sockets = {}
    MAX_BUFFER = 1024 * 640 

    def _get_connection_id(self):
        return self.path.split('/')[-1]

    def _get_socket(self):
        """get the socket which connects to the target address for this connection
        """
        id = self._get_connection_id()
        return self.sockets[id] 

    def _close_socket(self):
        """ close the current socket
        """
        id = self._get_connection_id()
        s = self.sockets[id]
        if s:
            s.close()

    def do_GET(self):
        """GET: Read data from TargetAddress and return to client through http response
        """
        s = self._get_socket()
        if s:
            data = s.recv(self.MAX_BUFFER)
            print data
            self.send_response(200)
            self.end_headers()
            self.wfile.write(data)
        else:
            print 'Connection With ID %s has not been established' % self._get_connection_id()

    def do_POST(self):
        """POST: Create TCP Connection to the TargetAddress 
        """
        id = self._get_connection_id() 
        print 'Initializing connection with ID %s' % id
        length = int(self.headers.getheader('content-length'))
        req_data = self.rfile.read(length)
        params = cgi.parse_qs(req_data, keep_blank_values=1) 
        target_host = params['host'][0]
        target_port = int(params['port'][0])

        print 'Connecting to target address: %s % s' % (target_host, target_port)
        #open socket connection to remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target_host, target_port))
        print 'Successfully connected'
        #save socket reference
        self.sockets[id] = s
        try: 
            self.send_response(200)
        except socket.error, e:
            print e

    def do_PUT(self):
        """Read data from HTTP Request and send to TargetAddress
        """
        id = self._get_connection_id()
        s = self.sockets[id]
        length = int(self.headers.getheader('content-length'))
        data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)['data'][0] 
        print 'Writing....'
        print data
        s.sendall(data)
        self.send_response(200)
        
    def do_DELETE(self): 
        self._close_socket()
        self.send_response(200)

def run_server(server_class=HTTPServer, handler_class=ProxyRequestHandler): 
    server_address = ('', 8888)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
