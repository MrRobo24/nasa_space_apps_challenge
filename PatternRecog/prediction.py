# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 11:48:22 2019

@author: mr_ro
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog")
df = pd.read_csv("india_v2.csv",index_col = 0)
data = np.array(df.loc[:,"latitude":"longitude"])
#plotting the data
plt.scatter(data[:,1],data[:,0], label='True Position')
    

#data = data[0:10000]
#backup code for 10 clusters
#creating the kmeansObject
kmeansObj = KMeans(n_clusters=200)
#fitting our data with the kmeansObject
kmeansObj.fit(data)

#printing centroid coordinates
print(kmeansObj.cluster_centers_)
#printing the labels assigned to the coordinates
plt.figure(dpi = 1200)
plt.savefig('map_50_clusters.png')
plt.scatter( data[:,1], data[:,0],c=kmeansObj.labels_, cmap='rainbow')
plt.scatter(kmeansObj.cluster_centers_[:,1],kmeansObj.cluster_centers_[:,0] , color='black')

centers = kmeansObj.cluster_centers_
labels = kmeansObj.labels_
os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/output_cluster_200")
pd.DataFrame(centers).to_csv("centers.csv",index = False)
pd.DataFrame(labels).to_csv("labels.csv",index = False)


#print(len(data))