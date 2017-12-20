# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 18:46:30 2017

@author: summer
"""
import pymysql.cursors
import socket
import sys

def ConnectDB():
    conn = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = None,
                             db = 'car_map_data',
                             charset = 'utf8')
    return conn

def updateDB(MAPDATA):
    #DBCONN = ConnectDB()
    DBCONN = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = None,
                             db = 'car_map_data',
                             charset = 'utf8')
    with DBCONN.cursor() as cursor:
            sql = 'UPDATE map SET car = %s, parked = %s WHERE x = %s and y = %s'
            cursor.execute(sql, (MAPDATA[2], MAPDATA[3], MAPDATA[0], MAPDATA[1]))
            DBCONN.commit()
            DBCONN.close()
            
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
    data = '0:1:0:0'
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
        data = read(s).decode('utf-8')
        print('data is received')
        print(' %s' % data)
        splitDatas(data.split(','))
        
def thread(s):
    c, addr = s.accept()
    sendData(c, addr)
    readData(c)
        
        
if __name__ == '__main__':
    port = 12345
    port2 = 32000
    s = Binding(port)
    s2 = Binding(port2)
    while True:
        thread(s)
        print(port)
        #thread(s2)
        #print(port2)
        