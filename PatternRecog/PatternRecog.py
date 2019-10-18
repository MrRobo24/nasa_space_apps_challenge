# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:52:45 2019

@author: mr_ro
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2, whiten
import math
import requests

os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog")
indiaCSV = pd.read_csv("india_v2.csv")
coordinates = np.array(indiaCSV.loc[:,"latitude":"longitude"])
"""
defining the coordinate which we are going to use as reference
"""
row = 0
latRef =0# indiaCSV.loc[row,"latitude"]	
longRef =0# indiaCSV.loc[row,"longitude"]

"""
#method1 to print several csv files for ref coordinates

distRad = math.sqrt(0.0019)
print("distRad",distRad)
xDiff = yDiff = 0.0
xList = indiaCSV.loc[:,"latitude"]
yList = indiaCSV.loc[:,"longitude"]
coordList = indiaCSV.loc[:,"latitude":"longitude"]

i = 0
j = 0
latTemp = longTemp = 0
distTemp = 0
for i in range(0,500):
    row = i
    latRef = indiaCSV.loc[row,"latitude"]	
    longRef = indiaCSV.loc[row,"longitude"]
    print("REF COORD: INDEX ",i," = ",latRef," ",longRef)
    print("")
    #missing here
    
    
    
    df = pd.DataFrame({"latitude":[], "longitude":[]})     
    for j in range(0,500) : 
        if j!=i:
            latTemp = coordList.loc[j,"latitude"]
            longTemp = coordList.loc[j,"longitude"]
            xDiff = (latRef - latTemp)**2
            yDiff = (longRef - longTemp)**2
            distTemp = math.sqrt(xDiff+yDiff)
            
            if distTemp <= distRad:
                print(coordList.iloc[j,:])
                series = coordList.iloc[j,:]
                df = df.append(series) #appending in temp dataframe
                print(" ")
    
    name = "REF_"+str(i)+".csv"
    df.to_csv(name)            
    print("DONE")
    print("")
    #df = df.append(pd.DataFrame({"latitude":[], "longitude":[]}) )
"""
"""
coordinates = np.array(indiaCSV.loc[:,"latitude":"longitude"])
x, y = kmeans2(whiten(coordinates),)
kmeans2()
"""

def funcUserData():
    userLat = float(input("Enter the latitude"))
    userLong = float(input("Enter the Longitude"))
    userMonth = float(input("Enter the Month"))
    
    userDataList = [userLat,userLong,userMonth]
    return userDataList

def funcFindCoords(userDataList):
    areaList = []
    distRad = 3
    userCoord = userDataList[0:2]
    distTemp = 0
    for i in range(0,len(coordinates)):
        latTemp = coordinates[i][0]
        longTemp = coordinates[i][1]
        distTemp = math.sqrt((latTemp - userCoord[0])**2 + (longTemp - userCoord[1])**2)*111
        if distTemp <= distRad:
            areaList.append([i,coordinates[i][0],coordinates[i][1],distTemp])
    
    return areaList

def funcFindProb(indexList,userDataList):
    
    prob = 0.00
    monthCounter = 0
    monthUser = userDataList[2]
    for index in indexList:
        monthTemp = indiaCSV.loc[index,"months"]
        if monthTemp == monthUser:
            monthCounter = monthCounter + 1
    
    prob = monthCounter / len(indexList)
    
    
    return prob
                


"""
#calling part of the code
for j in range(0,500):
    
    userDataList =  [indiaCSV.loc[j,"latitude"],indiaCSV.loc[j,"longitude"],indiaCSV.loc[j,"months"]]     #funcUserData()
    areaList = funcFindCoords(userDataList)
    #print(areaList)
    
    indexList = []
    for i  in areaList:
        indexList.append(i[0])
    
    prob = funcFindProb(indexList,userDataList)
    print("index ",j,": Prob = ",prob*100," %")

"""

df = pd.read_csv("india_copy.csv")
ans = 0
for i in range(0,1000):
    userDataRow = [df.loc[i,"latitude"],df.loc[i,"longitude"],int(df.loc[i,"acq_date"].split("/")[0])]
    
    userDataList = userDataRow    #funcUserData()
    areaList = funcFindCoords(userDataList)
    #print(areaList)
    indexList = []
    for i  in areaList:
        indexList.append(i[0])
        
    prob = funcFindProb(indexList,userDataList)
    ans = ans + prob
    #print("DATA: ",userDataRow," Prob = ",prob*100," %")

print(ans/1000)

coordDF = pd.DataFrame(areaList)
coordDF.to_csv("area.csv",index = False)










    

    
