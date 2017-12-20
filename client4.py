# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:12:34 2017

@author: summer
"""

import socket
import sys

def read(port):
    s = socket.socket()
    host = '192.168.0.14' #(IP address of PC (server))
    s.connect((host,port))
    try:
        msg = s.recv(1024)
        s.close()
    except socket.error as msg:
        sys.stderr.write('error %s' %msg[1])
        s.close()
        print('close')
        sys.exit(2)
    return msg

if __name__ == '__main__':
    port = 12345
    while True:
        print('hey, checking TCP socket')
        data = read(port)
        print('i just read %s' % data)
        print('port num is: %d' % port)
        port = port + 1
        