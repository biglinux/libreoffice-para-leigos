#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import http.server
import socketserver
import socket
from contextlib import closing
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, QSize
from configparser import ConfigParser

def http_server(port):
    handler = http.server.SimpleHTTPRequestHandler
    socketserver.TCPServer.allow_reuse_address = True
    tcpserver = socketserver.TCPServer(('', port), handler)
    try:
        tcpserver.serve_forever()
    except:
        pass

def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

def main():
    server_created = False

    # Start Server
    port = get_open_port()
    server = Process(target=http_server, args=(port,))
    server.start()

    print("Server Started on Port ", port)

    # Create application QT and create WebView
    app = QApplication([])
    web = QWebView()

    # Set Title
    web.setWindowTitle("Libreoffice Para Leigos")

    # Set icon
    icon = QIcon()
    icon.addFile('../icons/libreoffice-para-leigos.svg', QSize(48,48))
    web.setWindowIcon(icon)

    # Get dimensions from config file
    config = ConfigParser()
    configFilePath = os.getenv("HOME") + "/.libreoffice-para-leigos/conf"
    width, height = 800, 600
    x = y = None
    maximized = True
    if os.path.exists(configFilePath):
        config.read(configFilePath)
        maximized = False
        width = config.get('window','width') if config.has_option('window','width') else width
        height = config.get('window','height') if config.has_option('window','height') else height
        x = config.get('window','x') if config.has_option('window','x') else x
        y = config.get('window','y') if config.has_option('window','y') else y

    else:
        basedir = os.path.dirname(configFilePath)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        config.add_section('window')

    # Define geometry
    web.resize(int(width), int(height))

    # center window
    if(x is None or y is None):
        web.move(app.desktop().screen().rect().center() - web.rect().center())
    else:
        web.move(int(x), int(y))

    # Debug
    if "--debug" in sys.argv:
        from PyQt5.QtWebKit import QWebSettings
        web.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        web.page().mainFrame().evaluateJavaScript("var debug=true;")

    # Load Page
    html = QUrl('http://127.0.0.1:%i/app/web/viewer.html'%(port))
    web.load(html)

    if maximized:
        web.showMaximized()
    else:
        web.show()

    # Stop Server, Save window config and Quit
    ret = app.exec_()
    server.terminate()
    config.set('window', 'width', str(web.frameGeometry().width()))
    config.set('window', 'height', str(web.frameGeometry().height()))
    config.set('window', 'x', str(web.geometry().x()))
    config.set('window', 'y', str(web.geometry().y()))
    with open(configFilePath, 'w') as file:
        config.write(file)
    sys.exit(ret)

if __name__ == '__main__':
    main()
