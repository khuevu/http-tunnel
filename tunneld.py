#!/usr/bin/env python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer 
import socket
import cgi

class ProxyRequestHandler(BaseHTTPRequestHandler):
    sockets = {}
    MAX_BUFFER = 1024 * 32

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
            print remote_data
            self.send_response(200)
            self.end_headers()
            self.wfile.write(remote_data)
        else:
            print 'connection has not been established'

    def do_POST(self):
        """Create TCP Connection with the RemoteAddr
        """
        id = self._get_connection_id() 
        print 'connection id %s' % id
        #ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        length = int(self.headers.getheader('content-length'))
        req_data = self.rfile.read(length)
        remote_add = cgi.parse_qs(req_data, keep_blank_values=1) 
        print remote_add
        remote_host = remote_add['host'][0]
        remote_port = int(remote_add['port'][0])
        print 'Remote address %s % s' % (remote_host, remote_port)
        #open socket connection to remote server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((remote_host, remote_port))
        print 'open connection to remote server'
        self.sockets[id] = s
        #return status ok
        try: 
            self.send_response(200)
        except socket.error, e:
            print e

    def do_PUT(self):
        """Read data from HTTP Request and send over TcpConnection to RemoteAddr
        """
        id = self._get_connection_id()
        s = self.sockets[id]
        length = int(self.headers.getheader('content-length'))
        send_data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)['data'][0] 
        print 'Recv tunneled write data'
        print send_data
        s.sendall(send_data)
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
