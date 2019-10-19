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
url='https://firms.modaps.eosdis.nasa.gov/data/active_fire/viirs/csv/VNP14IMGTDL_NRT_South_Asia_24h.csv'
response = requests.get(url)
with open(os.path.join("downloaded_data.csv"), 'wb') as f:
    f.write(response.content)
    
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
hostname = "192.168.137.130"
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
    message = str((df.iloc[coordDF.loc[iMin,0],0:2].values)[0]) +" "+ str((df.iloc[coordDF.loc[iMin,0],0:2].values)[1]) + " "+str(minDis)

else:
    print("NO AREA")
    message = "0 0 0"

message = message + "\n"
#sending
s2 = socket.socket()

#hostname = "DESKTOP-L6VTJ5H"
hostname2 = "192.168.137.130" #aryan
#hostname2  = "192.168.137.164 "   #arpit 
port2 = 8050


s2.connect((hostname2,port2))
s2.send(message.encode())


#s.send(message.encode())
print("sent to receiving server of aryan")




    

    
