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


#188 me garbar
for i in range(0,200):
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/zones")
    zonename = "zone_"+str(i)+".csv"
    zonedf = pd.read_csv(zonename)
    zonedf = zonedf.convert_objects(convert_numeric=True)
    data = np.array(zonedf.loc[:,"latitude":"longitude"])
    data = np.delete(data, np.argwhere(np.isnan(data)), axis=0)
    #fitting our data with the kmeansObject
    #needs improvement
    kmeansObj = KMeans(n_clusters=200)
    #kmeansObj = KMeans(n_clusters=10)
    kmeansObj.fit(data)
    #plt.figure(dpi = 1200)
    #plt.savefig('map_50_clusters.png')
    #plt.scatter( data[:,1], data[:,0],c=kmeansObj.labels_, cmap='rainbow')
    #plt.scatter(kmeansObj.cluster_centers_[:,1],kmeansObj.cluster_centers_[:,0] , color='black')
    #assigning centers and labels for this cluster
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/subzones")
    centers = kmeansObj.cluster_centers_
    labels = kmeansObj.labels_
    centersname = "subzone_centers_"+str(i)+".csv"
    labelsname =  "subzone_labels_"+str(i)+".csv"
    subfoldername  =  "subzone_" + str(i)
    os.mkdir(subfoldername)
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/subzones/"+subfoldername)
    pd.DataFrame(centers).to_csv(centersname,index = False)
    pd.DataFrame(labels).to_csv(labelsname,index = False)
    print(subfoldername," written \n")

