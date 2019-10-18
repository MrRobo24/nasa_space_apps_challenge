# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 16:43:09 2019

@author: mr_ro
"""
import socket

s = socket.socket()
hostname = "DESKTOP-L6VTJ5H"
port = 8080

s.connect((hostname,port))
x = ""
while True:
    #x = df_string#input("Enter Message: ")
    #receiving data from server
    x = s.recv(1024000).decode()
    if not x == "":
        print("DATA RECEIVED")
        break


#sample = "24.22323 62.2322"
currentCoord = x.split(" ")
currentCoord = list(map(float, currentCoord))

print(currentCoord, " DONE")