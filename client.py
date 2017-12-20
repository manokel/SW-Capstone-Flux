# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 19:12:34 2017

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
        

def read(port):
    s = socket.socket()
    host = '192.168.0.18'
    s.connect((host,port))
    try:
        msg = s.recv(4096)
        s.close()
    except socket.error as msg:
        sys.stderr.write('error %s' %msg[1])
        s.close()
        print('close')
        sys.exit(2)
    return msg

def splitDatas(MAPSECTOR):
    for i in range(len(MAPSECTOR)):
            MAPDATA = MAPSECTOR[i].split(':')
            updateDB(MAPDATA)
            
def readData(port):
        print('data is received')
        data = read(port).decode('utf-8')
        print(' %s' % data)
        splitDatas(data.split(','))
        DBCONN.close()
        print('port num is: %d' % port)
        

if __name__ == '__main__':
    port = 12345
    while True:
        readData(port)
        port = port + 1
        break
        
        