# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 22:34:25 2019

@author: mr_ro
"""

import os
import pandas as pd

subzoneDF = pd.DataFrame()

for i in range(0,200):
    foldername = "subzone_" + str(i)
    filename = "subzone_centers_" + str(i) + ".csv"
    os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/subzones/" + foldername)
    subzoneDF = subzoneDF.append(pd.read_csv(filename))

os.chdir("C:/Users/mr_ro/Documents/GitHub/nasa_space_apps_challenge/PatternRecog/")
subzoneDF.to_csv("subzoneCentersCombined.csv",index = False)

    