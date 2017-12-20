# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 20:54:55 2017

@author: summer
"""
import socket
import sys

Sector00 = '0:0:0:0:0:0:0'
Sector01 = '0:1:0:0:0:0:0'
Sector02 = '0:2:0:0:0:0:0'
Sector03 = '0:3:0:0:0:0:0'
Sector04 = '0:4:0:0:0:0:0'
Sector11 = '1:1:0:0:1:0:0'
Sector12 = '1:2:1:0:0:0:0'
Sector13 = '1:3:0:0:1:0:0'


def Connecting(port):
    s = socket.socket()
    host = '192.168.0.14'
    s.connect((host,port))
    s.listen(5)
    return s
    
def sendData(c, addr):
    print('starting sending data')
    words = Sector00 +','+ Sector01 + ',' + Sector02 + ',' + Sector03 + ',' + Sector04 + ',' + Sector11 + ',' + Sector12 + ',' + Sector13
    # x, y, park, car, obstacle, led, parked
    data = words
    print('send data: %s' % data)
    words = 'I am raspberry Pi (1) get this data'
    byte_data = str.encode(data)
    c.sendall(byte_data)
    
def readData(s):
    try:
        msg = s.recv(2048)
        print('i get it your data thx')
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
        s = Connecting(port)
        c, addr = s.accept()
        sendData(c, addr)
        readData(s)
        port = port + 1