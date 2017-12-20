#python3

import socket

HOST = '192.168.18.5'
PORT = 12348

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
msg=input()
s.send(msg.encode(encoding='utf_8', errors='strict'))
data = s.recv(1024)
print ('result: ' + data.decode())

s.close()