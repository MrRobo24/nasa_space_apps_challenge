# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 01:30:03 2019

@author: mr_ro
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from sklearn.preprocessing import MinMaxScaler #for scling data



#188 me garbar
factor = 50/2369
for i in range(188,200):
    os.chdir("C:/Users/Robin Singh/Desktop/NASA/zones")
    zonename = "zone_"+str(i)+".csv"
    zonedf = pd.read_csv(zonename)
    zonedf = zonedf.convert_objects(convert_numeric=True)
    data = np.array(zonedf.loc[:,"latitude":"longitude"])
    data = np.delete(data, np.argwhere(np.isnan(data)), axis=0)
    #fitting our data with the kmeansObject
    #needs improvement
    '''kmeansObj = KMeans(n_clusters=200)
    #kmeansObj = KMeans(n_clusters=10)
    kmeansObj.fit(data)'''
    #mms = MinMaxScaler()
    #mms.fit(data)
    
    #scaling data started
    maxLat = data[:,0].max()
    minLat = data[:,0].min()
    data[:,0] = np.divide(data[:,0],maxLat-minLat)
    maxLong = data[:,1].max()
    minLong = data[:,1].min()
    data[:,1] = np.divide(data[:,1],maxLong-minLong)
    #scaling data ended
    data_transformed = data#mms.transform(data)
    data_transformed = pd.DataFrame(data_transformed, columns=['Longitude','Latitude'])
    n_clusters = int(len(data_transformed)*factor)
    if n_clusters > 90:
        n_clusters = 90
    if i == 188:
        n_clusters = 5
    km = KMeans(n_clusters,max_iter = 500)
    km = km.fit(data_transformed)
    data_transformed.plot(kind='scatter',x='Longitude',y='Latitude',c=km.labels_, cmap='rainbow')
    #plt.figure(dpi = 1200)
    #plt.savefig('map_50_clusters.png')
    #plt.scatter( data[:,1], data[:,0],c=kmeansObj.labels_, cmap='rainbow')
    #plt.scatter(kmeansObj.cluster_centers_[:,1],kmeansObj.cluster_centers_[:,0] , color='black')
    #assigning centers and labels for this cluster
    os.chdir("C:/Users/Robin Singh/Desktop/NASA/subzones")
    centers = np.array(km.cluster_centers_)
    labels = np.array(km.labels_)
    centers[:,0] = np.multiply(centers[:,0],maxLat-minLat)
    centers[:,1] = np.multiply(centers[:,1],maxLong-minLong)
    centersname = "subzone_centers_"+str(i)+".csv"
    labelsname =  "subzone_labels_"+str(i)+".csv"
    subfoldername  =  "subzone_" + str(i)
    os.mkdir(subfoldername)
    os.chdir("C:/Users/Robin Singh/Desktop/NASA/subzones/"+subfoldername)
    pd.DataFrame(centers).to_csv(centersname,index = False)
    pd.DataFrame(labels).to_csv(labelsname,index = False)
    print(subfoldername," written \n")
    
    


