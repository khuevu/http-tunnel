HTTP TUNNEL
==========

Tunneling TCP connection through HTTP

Example Usage: 

To start a tunnel client which target to irc.freenode.net:6667

    python tunnel.py -p 8765 -r 127.0.0.1:8998 irc.freenode.net:6667

Start the tunneld server on a remote machine which will direct connection to
the target

    python tunneld.py -p 8998

To test the IRC connection via the tunnel: 

    nc 127.0.0.1 8765
    NICK abc

Credit: 
This project was inspired by [supertunnel
project](https://code.google.com/p/supertunnel/)


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/khuevu/http-tunnel/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

