# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 01:28:23 2019

@author: mr_ro
"""


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/output_cluster_200")

os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog")
df = pd.read_csv("india_v2.csv",index_col = 0)
data = np.array(df.loc[:,"latitude":"longitude"])
plt.figure(figsize=(100, 100), dpi=40)
plt.figure(dpi = 600)
plt.scatter( data[:,1], data[:,0])
i = 10
os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/zones")
zonename = "zone_"+str(i)+".csv"
zonedf = pd.read_csv(zonename)
zonedf = zonedf.convert_objects(convert_numeric=True)
data = np.array(zonedf.loc[:,"latitude":"longitude"])
data = np.delete(data, np.argwhere(np.isnan(data)), axis=None)
#data = np.nan_to_num(data)
#fitting our data with the kmeansObject
kmeansObj = KMeans(n_clusters=200)
#kmeansObj = KMeans(n_clusters=10)
kmeansObj.fit(data)
plt.scatter( data[:,1], data[:,0],c=kmeansObj.labels_, cmap='rainbow')

print(data)