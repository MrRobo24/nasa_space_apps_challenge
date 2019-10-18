# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:21:30 2019

@author: mr_ro
"""
import socket
#import os
#os.system("report_fire.py 1")

#experiments

listensocket = socket.socket()
Port = 8000
Port2 = 8080
maxConnections = 999

listensocket2 = socket.socket()
listensocket2.bind(("",Port2))
listensocket2.listen(maxConnections)


IP = socket.gethostname()

listensocket.bind(("",Port))

listensocket.listen(maxConnections)
print("Server started initially for receiving at "+ IP + " on port" + str(Port))

(clientsocket, address) = listensocket.accept()
print("New connection made1")
print("ADDRESS: ",address)

running =  True
message = ""

while running:
    message = clientsocket.recv(1024).decode()
    #ans = pd.read_json(message)
    if not message == "":
        print("Message Recieved from device")
        break

print("Server started initially for interacting with client at "+ IP + " on port" + str(Port))


(clientsocket2, address2) = listensocket2.accept()
print("New connection made2 for sending")
clientsocket2.send(message.encode())
print("Message from device was sent to client")

message = ""
while running:
    message = clientsocket2.recv(1024).decode()
    #ans = pd.read_json(message)
    if not message == "":
        print("Message Recieved from client")
        break

#message.encode()
message = message + "\n"
clientsocket.send(message.encode())
print("Message sent to device")

listensocket.close()
listensocket2.close()

print("Done")

"""
#sample = "24.22323 62.2322"
currentCoord = message.split(" ")
currentCoord = list(map(float, currentCoord))

print(currentCoord, " DONE")
ans = "arpit"
clientsocket.send(ans.encode())
"""