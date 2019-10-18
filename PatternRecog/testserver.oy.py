# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 21:23:55 2019

@author: mr_ro
"""

import socket

HOST = socket.gethostname()
PORT = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as err:
    print('Bind failed. Error Code : ' .format(err))
s.listen(10)
print("Socket Listening")
conn, addr = s.accept()
while(True):
    
    data = conn.recv(1024)
    print(data.decode(encoding='UTF-8'))
    conn.send(bytes("Message"+"\r\n",'UTF-8'))
    print("Message sent")