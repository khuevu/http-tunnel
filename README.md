HTTP TUNNEL
==========

A program to tunnel TCP connection through HTTP connection

## Usage: 

The program is useful when you has a client behind a firewall which only allows
HTTP connections or connections to standard ports such as port 80 of HTTP. You
will need a remote server outside of the firewall. 

### Tunnel Server 

Start the tunneld server on a remote machine. The server listens on a port
specified by parameter `-p` for HTTP connection from a client program. 

    python tunneld.py -p <listen_port> 

The server then read the HTTP payload and send it to the target using TCP
connection. The target is specified by the client when establishing the tunnel. 

Usually, tunneling will actually be useful when you use the default HTTP port
80 so that the connection from tunnel client to tunnel server is not blocked by
firewall. 

### Tunnel Client 

Start the tunnel client which listen on the local machine. The command needs
local port parameter, the remote tunnel server and its port, and the target that the client want to connect to.

    python tunnel.py -p <client_port> -r <tunnel_server_host>:<tunnel_server_port> <target_host>:<target_port>

When this command is executed, the client sends a http request to establish the
tunnel with the remote tunnel server. The tunnel server will then establish
a TCP connection with the target server. 

### Example

To connect to irc server using the tunnel:

    # 1. on server machine (remote_host)
    python tunneld.py -p 80

    # 2. on client machine: 
    python tunnel.py -p 8765 -r remote_host:80 irc.freenode.net:6667

    # 3. on the client machine, test the tunnel connection using netcat
    nc 127.0.0.1 8765
    # send irc NICK command to the connection and see the response back from
    the irc server
    NICK abc

## Credit: 

This project was inspired by [supertunnel
project](https://code.google.com/p/supertunnel/)
