# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 15:27:26 2019

@author: mr_ro
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 21:53:03 2019

@author: mr_ro
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

#loading the CSVs
os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/output_cluster_200")
centroids_df = pd.read_csv("centers.csv")
labels_df = pd.read_csv("labels.csv")
os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog")
df = pd.read_csv("india_v2.csv",index_col = 0).sort_values(by=["latitude"])
os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/zones")
#experiment
areaDfList = []

for i in range(0,200):
    areaDfList.append(pd.DataFrame([]))
    
for i in range(0,100000):
    areaDfList[labels_df.iloc[i,0]] = areaDfList[labels_df.iloc[i,0]].append([df.iloc[i,:]])

for i in range(0,200):
    name = "zone_" + str(i) + ".csv"
    areaDfList[i].to_csv(name,mode = 'a',index = False)

