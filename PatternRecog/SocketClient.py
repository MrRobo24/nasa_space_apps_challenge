# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 23:28:23 2019

@author: mr_ro
"""
#import os
#import pandas as pd
import socket
s = socket.socket()

hostname = "DESKTOP-L6VTJ5H"
port = 8080

#experimenting
#os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/output_cluster_200")
#centersDf = pd.read_csv("centers.csv")
#print(centersDf)
#df_string = centersDf.to_json()

s.connect((hostname,port))
while True:
    ans  = s.recv(1024)
    if not ans == "":
        ans = ans.decode()
        break
    
print(ans)

message = "RETURN ANS"
s.send(message.encode())
print("DONE")





