# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 23:08:14 2019

@author: mr_ro
"""
import os
import pandas as pd
import numpy as np
import math
import requests
import socket
#import time

os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog")
"""
url='https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_South_Asia_24h.csv'
response = requests.get(url)
with open(os.path.join("downloaded_data.csv"), 'wb') as f:
    f.write(response.content)
"""
df = pd.read_csv("downloaded_data.csv")    

coordinates = np.array(df.loc[:,"latitude":"longitude"])


def funcFindCoords(userDataList):
    areaList = []
    distRad = 3
    userCoord = userDataList[0:2]
    distTemp = 0
    for i in range(0,len(coordinates)):
        latTemp = coordinates[i][0]
        longTemp = coordinates[i][1]
        distTemp = 111*math.sqrt(((latTemp - userCoord[0])**2) + ((longTemp - userCoord[1])**2))
        if distTemp <= distRad:
            areaList.append([i,coordinates[i][0],coordinates[i][1],distTemp])
            
    
    return areaList
                

print("DATA DOWNLOADED")

s = socket.socket()
#hostname = "DESKTOP-L6VTJ5H"
hostname = "192.168.43.22"
port = 8090

#experimenting
#os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/output_cluster_200")
#centersDf = pd.read_csv("centers.csv")
#print(centersDf)
#df_string = centersDf.to_json()

s.connect((hostname,port))

while True:
    print("Receiving Started")
    message  = s.recv(1024)
    if not message == "":
        message = message.decode()
        print("Coordinates received from device")
        break

#receiving data
"""
#experiment
try:
    message = s.recv(8192)
    if not message == "":
        print(message)
        #change the beginning time for measurement
        begin=time.time()
    else:
        #sleep for sometime to indicate a gap
        time.sleep(0.1)
except:
    pass




#experiment end

"""

#hardcoded
#message = "30.84795 79.37023 2"

#sample = "24.22323 62.2322"
#message = "0 0"
currentCoord = message.split(" ")
currentCoord = list(map(float, currentCoord))



userDataList = currentCoord    #funcUserData()
areaList = funcFindCoords(userDataList)
#print(areaList)
indexList = []
for i  in areaList:
    indexList.append(i[0])

coordDF = pd.DataFrame(areaList)
if(len(coordDF)>0):
    coordDF.to_csv("area.csv",index = False)
    #print(coordDF.iloc[:,3])
    
    minDis = coordDF.loc[0,3]
    iMin = 0
    for i in range(0,len(coordDF)):
        if coordDF.loc[i,3]< minDis:
            iMin = i
            minDis = coordDF.loc[i,3]
    
    
    #coordDF.loc[[iMin]].to_csv("fire_at_min_dis.csv",index = False) #for printing only the coordinates and distance
    df.loc[[coordDF.loc[iMin,0]]].to_csv("fire_at_min_dis.csv",index = False) #to print all the details of that fire
    
    confidence = df.iloc[coordDF.loc[iMin,0],8]
    if confidence == "high":
        confidence = 1
    elif confidence == "nominal":
        confidence = 0.5
    else:
        confidence = 0.25
    
    
    message1 = str((df.iloc[coordDF.loc[iMin,0],0:2].values)[0]) +" "+ str((df.iloc[coordDF.loc[iMin,0],0:2].values)[1]) +" " + str(df.iloc[coordDF.loc[iMin,0]:]) +" "+str(minDis+str(confidence))

else:
    print("NO AREA")
    message1 = "24.22323 62.2322 0.2344 0.5 "
    """
os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog")
dfTOT = pd.read_csv("downloaded_data.csv")
lat,long = currentCoord[0],currentCoord[1]

df = pd.DataFrame()
for i in range(0,len(dfTOT)):
    latTemp = dfTOT.iloc[i,0]
    longTemp = dfTOT.iloc[i,1]
    
    disTemp = 111*math.sqrt((latTemp - lat)**2 + (longTemp - long)**2)
    if disTemp < 100:
        print(dfTOT.iloc[i,0])
        l = [[dfTOT.iloc[i,0],dfTOT.iloc[i,1]]]
        df = df.append(l)

df.to_csv("current_zone.csv")
if len(df>0):
    message = ""
    for i in range(0,len(df)):
        message = message + str(df.iloc[i,0]) + "," + str(df.iloc[i,1])
        if not i == len(df) - 1:
            message = message + " "
            
    message = "0,1 " + message + "\n"
else:
    message  = "0,1 0,0\n"
    
message = message1 +  message

    



"""


message1 = message1 + "\n"
#sending
s2 = socket.socket()

#hostname = "DESKTOP-L6VTJ5H"
hostname2 = "192.168.43.22" #aryan
#hostname2  = "192.168.137.164 "   #arpit 
port2 = 8050


s2.connect((hostname2,port2))
s2.send(message1.encode())


#s.send(message.encode())
print("sent to receiving server of aryan")




    

    
