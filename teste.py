#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#from subprocess import Popen, PIPE, STDOUT

#try:
#    from subprocess import DEVNULL # py3k
#except ImportError:
#    import os
#    DEVNULL = open(os.devnull, 'wb')

#ps = Popen(["python3", "-m", "http.server", "8001", "--bind", "127.0.0.1"], stdout=DEVNULL, stderr=STDOUT)

#print(ps.pid)

#Popen(["kill", "-9", str(ps.pid)], stdout=DEVNULL, stderr=STDOUT)

#text = u"René Descartes"
#p = Popen(['espeak', '-b', '1'], stdin=PIPE, stdout=DEVNULL, stderr=STDOUT)
#p.communicate(text.encode('utf-8'))
#assert p.returncode == 0 # use appropriate for your program error handling here




#import http.server
#import socketserver

#PORT = 8000

#Handler = http.server.SimpleHTTPRequestHandler

#httpd = socketserver.TCPServer(("", PORT), Handler)

#print("serving at port", PORT)
#httpd.serve_forever()

#ret = app.exec_()
#http.shutdown()
#sys.exit(ret)

import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
