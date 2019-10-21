# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 11:53:46 2019

@author: mr_ro
"""

import os
from datetime import date
import pandas as pd
import numpy as np
#from sklearn.feature_selection import VarianceThreshold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
#from sklearn import svm
from sklearn.metrics import r2_score
import socket
import math
#import matplotlib.pyplot as plt


#from sklearn.ensemble import RandomForestClassifier
#from sklearn.metrics import accuracy_score, confusion_matrix

s = socket.socket()
#hostname = "DESKTOP-L6VTJ5H"
hostname = "192.168.43.22"
port = 7000


s.connect((hostname,port))


while True:
    print("Receiving started")
    message  = s.recv(1024)
    if not message == "":
        message = message.decode()
        print("Coordinates received from device")
        break

#message = "30.84795 79.37023 2"
#message = "31.74 75.268 2"
currentCoord = message.split(" ")
currentCoord = np.delete((np.array(list(map(float, currentCoord)))).astype(float),-1)
if (currentCoord[0] > 32.20 or currentCoord[0] < 8.00) or (currentCoord[1] > 96.20 or currentCoord[1] < 68.76):
    print("Your location is out of our reach or doesn't experince frequent fire")
    prediction = 0.0
else:
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/output_cluster_200")
    zoneCentersDF = pd.read_csv("centers.csv")
    distMin = 9999999
    jMin = 0
    for j in range(0,len(zoneCentersDF)):
        zoneCoord = (np.array([zoneCentersDF.iloc[j,0],zoneCentersDF.iloc[j,1]])).astype(float)
        dist = zoneCoord - currentCoord
        dist =  math.sqrt(np.sum(np.square(dist)))
       # print(dist)
        if dist < distMin:
            distMin = dist
            jMin = j
    
    zoneLabelsDF = pd.read_csv("labels.csv")
    zoneNo = zoneLabelsDF.iloc[jMin,0]
    print("Zone No. =  ", zoneNo)
    name = "subzone_" + str(zoneNo)
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/subzones/"+name)
    name = "subzone_centers_" + str(zoneNo) +".csv"
    print("dIST ZONE ", distMin)
    subzoneCentersDF = pd.read_csv(name)
    distMin = 9999999
    jMin = 0
    for j in range(0,len(subzoneCentersDF)):
        subzoneCoord = (np.array([subzoneCentersDF.iloc[j,0],subzoneCentersDF.iloc[j,1]])).astype(float)
        dist = subzoneCoord - currentCoord
        dist =  math.sqrt(np.sum(np.square(dist)))
        print(dist)
        if dist < distMin:
            distMin = dist
            jMin = j
    
    print("DSIISSSDSADAS ",distMin)


    
    index = jMin
    
    subzone_labels = pd.read_csv("subzone_labels_"+str(zoneNo)+".csv")
    subzone_no = subzone_labels.iloc[index,0]
    print("Sub Zone No: ",subzone_no)
    
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/zones")
    zone_data = pd.read_csv("zone_"+str(zoneNo)+".csv")
    Y = pd.DataFrame()
    for i in range(0,len(subzone_labels)):
        zone_temp = subzone_labels.iloc[i,0]
        if zone_temp == subzone_no:
            dataList = [[i ,zone_data.loc[i,"bright_t31"],zone_data.loc[i,"brightness"],zone_data.loc[i,"confidence"],zone_data.loc[i,"daynight"],zone_data.loc[i,"frp"],zone_data.loc[i,"months"]]]
            dataList = pd.DataFrame(dataList)
            Y = Y.append(dataList)
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/subzones/subzone_"+str(zoneNo))
    Y.to_csv("Y_"+str(zoneNo)+".csv",index = False)
    Ydf = pd.read_csv("Y_"+str(zoneNo)+".csv",index_col = 0)
    for i in range(0,len(Ydf)):
        if Ydf.iloc[i,3] == 'D':
            Ydf.iloc[i,3] = 1
        else:
            Ydf.iloc[i,3] = 0
            
    #feature scaling   
    Ydf = np.array(Ydf)
    for i in range(0,6):
        Ydf[:,i] = (Ydf[:,i] - Ydf[:,i].mean())/Ydf[:,i].max()
    """
    
    mean_0 = Ydf[:,0].mean()
    max_0 = Ydf[:,0].max()
    Ydf[:,0] = (Ydf[:,0] - mean_0)/max_0
    
    mean_1 = Ydf[:,1].mean()
    max_1 = Ydf[:,1].max()
    Ydf[:,1] = (Ydf[:,1] - mean_1)/max_1
    """
    # y = mul and X = months
    #y = np.array((Ydf[:,1] * Ydf[:,2] * Ydf[:,4] * Ydf[:,5]))
    y = np.array((Ydf[:,5]))#+Ydf[:,1]))#Ydf[:,0])) # frp and brightness
    X = np.array(Y.loc[:,6]) 
    
    labelencoder_y = LabelEncoder()
    y = labelencoder_y.fit_transform(y)
    #data loaded
    
    #splitting
    X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.2,random_state = 0)
    X_train= X_train.reshape(-1, 1)
    
    
    """
    
    #training classifier
    clf = svm.SVC(gamma = 0.001)
    clf.fit(X_train, y_train)  
            
    pr = clf.predict(X_test.reshape(-1,1))
    """
    #getting month input
    
    
    month = int(str(date.today()).split("-")[1])
    month = 10
    
    
    
    #regression
    """
    clf = svm.SVR(kernel = 'rbf')
    clf.fit(X_train, y_train)  
            
    
    """
    
    
    from sklearn import linear_model
    reg = linear_model.Ridge(alpha=0.9)
    reg.fit(X_train,y_train) 
    
    
    
    #testing
    reg.coef_
    reg.intercept_ 
    predictions = reg.predict(X_test.reshape(-1,1))
    print(reg.score(X_test.reshape(-1,1),y_test))
    print(r2_score(y_test,predictions))       
    
    #scaling y_train
    minY = y_train.min()
    maxY = y_train.max()
    y_train = (y_train - minY)/(maxY - minY)
    
    prediction = reg.predict([[month]])
    prediction = (prediction - minY)/(maxY - minY)
    
    if prediction > 1:
        print("Your zone doesn't experience frequent fires")
        prediction = 0.0
    else:
        print(prediction)
        

message = (str(prediction[0]*100)) + "\n"



 



#sending to mid server
s2 = socket.socket()
#hostname = "DESKTOP-L6VTJ5H"
hostname2 = "192.168.43.22" #arayn
#hostname2  = "192.168.137.164 "   #arpit 
port2 = 8050


s2.connect((hostname2,port2))
s2.send(message.encode())

"""
bright_t31
brightness
confidence
daynight
frp
months
"""


