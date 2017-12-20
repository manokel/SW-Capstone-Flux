# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 18:46:30 2017

@author: summer
"""
import pymysql.cursors
import socket
import sys

DBCONN = pymysql.connect(host = 'localhost',
                           user = 'root',
                           password = None,
                           db = 'car_map_data',
                           charset = 'utf8')


def updateDB(MAPDATA):
    with DBCONN.cursor() as cursor:
            sql = 'UPDATE map SET car = %s, parked = %s WHERE x = %s and y = %s'
            cursor.execute(sql, (MAPDATA[3], MAPDATA[6], MAPDATA[0], MAPDATA[1]))
            DBCONN.commit()
            
def Binding(port):
    s = socket.socket()
    host = ''
    s.bind((host,port))
    s.listen(5)
    return s

def splitDatas(MAPSECTOR):
    for i in range(len(MAPSECTOR)):
            MAPDATA = MAPSECTOR[i].split(':')
            updateDB(MAPDATA)

def sendData(c, addr):
    data = 'abcs '
    byte_data = str.encode(data)
    c.sendall(byte_data)
    
    
def read(s):
    try:
        msg = s.recv(1024)
        s.close()
    except socket.error as msg:
        sys.stderr.write('error %s' %msg[1])
        s.close()
        print('close')
        sys.exit(2)
    return msg

def readData(s):
        print('data is received')
        data = read(s).decode('utf-8')
        print(' %s' % data)
        #splitDatas(data.split(','))
        
def rpiPCcom(s):
        c, addr = s.accept()
        sendData(c, addr)
        readData(c)
        
        
if __name__ == '__main__':
    port = 12345
    port2 = 32000
    s = Binding(port)
    s2 = Binding(port2)
    while True:
        rpiPCcom(s)
        print(port)
        rpiPCcom(s2)
        print(port2)
        
        
