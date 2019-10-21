# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 04:58:02 2019

@author: mr_ro
"""

import os
import pandas as pd
import requests
import socket
#import time
import math
import numpy as np

os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog")
url='https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_South_Asia_24h.csv'
response = requests.get(url)
with open(os.path.join("downloaded_data2.csv"), 'wb') as f:
    f.write(response.content)

print("REALTIME DATA DOWNLOADED")
s = socket.socket()
#hostname = "DESKTOP-L6VTJ5H"
hostname = "192.168.137.130"
port = 9999

#experimenting
#os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/output_cluster_200")
#centersDf = pd.read_csv("centers.csv")
#print(centersDf)
#df_string = centersDf.to_json()

s.connect((hostname,port))

while True:
    print("Connected to Py server")
    print("Receiving Started")
    message  = s.recv(1024)
    if not message == "":
        message = message.decode()
        print("Coordinates received from device")
        break


#sample = "24.22323 62.2322 "
message = "20.30454 56.79476"
currentCoord = message.split(" ")
currentCoord = list(map(float, currentCoord))
lat,long = currentCoord[0],currentCoord[1]



dfTOT = pd.read_csv("downloaded_data.csv")

df = pd.DataFrame()
for i in range(0,len(dfTOT)):
    latTemp = dfTOT.iloc[i,0]
    longTemp = dfTOT.iloc[i,1]
    
    disTemp = 111*math.sqrt((latTemp - lat)**2 + (longTemp - long)**2)
    if disTemp < 100:
        print(dfTOT.iloc[i,0])
        l = [[dfTOT.iloc[i,0],dfTOT.iloc[i,1]]]
        df = df.append(l)


if len(df>0):
    message = ""
    for i in range(0,len(df)):
        message = message + str(df.iloc[i,0]) + "," + str(df.iloc[i,1])
        if not i == len(df) - 1:
            message = message + " "
            
    message = "0,1 " + message + "\n"
else:
    message  = "0\n"


#sending to mid server
s2 = socket.socket()
#hostname = "DESKTOP-L6VTJ5H"
hostname2 = "192.168.137.130" #arayn
#hostname2  = "192.168.137.164 "   #arpit 
port2 = 8050


s2.connect((hostname2,port2))
s2.send(message.encode())



s.close()
s2.close()



