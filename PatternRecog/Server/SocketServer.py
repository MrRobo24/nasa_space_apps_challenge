# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:21:30 2019

@author: mr_ro
"""
import pandas as pd
import socket
import time

listensocket = socket.socket()
Port = 8000
maxConnections = 999
IP = socket.gethostname()

listensocket.bind(("",Port))

listensocket.listen(maxConnections)
print("Server started at "+ IP + " on port" + str(Port))

(clientsocket, address) = listensocket.accept()
print("New connection made")

running =  True
message = ""
while running:
    message = clientsocket.recv(1024000).decode()
    ans = pd.read_json(message)
    if not message == None:
        print(message)
        break

#sorting because order is lost while encoding and decoding
ans = ans.sort_index()