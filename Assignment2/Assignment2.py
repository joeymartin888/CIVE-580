#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:10:23 2020

@author: Joseph Martin, University of Victoria
"""

import pandas as pd
import numpy as np

"""Sort the dataframes first into useable matrices!!"""

pin=pd.read_csv("/home/josmarti/Code/CIVE-580/Assignment1/1022571_Duncan_Glenora.csv")
qin=pd.read_csv("Cowichan_Duncan_monthlyQ.csv")
psorted=np.zeros((len(pin["Unnamed: 0"]),len(pin.columns)-1))
qsorted=np.zeros((len(qin["Unnamed: 0"]),len(qin.columns)))

for data in range(len(qin["Unnamed: 0"])):
    qsorted[data,1]=int(qin.loc[data,"Unnamed: 0"][5:7]) #making months useable integers
    if int(qin.loc[data,"Unnamed: 0"][5:7])<10: #to organize by water year 1 Oct - 30 Sep
        qsorted[data,0]=int(qin.loc[data,"Unnamed: 0"][0:4])-1 #making years useable integers
    else:
        qsorted[data,0]=int(qin.loc[data,"Unnamed: 0"][0:4]) #making years useable integers
    qsorted[data,2]=qin.loc[data,"Q_cms"]

for data in range(len(pin["Unnamed: 0"])):
    psorted[data,1]=pin.loc[data,"month"] #no int() needed as the values in this dataframe are already integers
    if pin.loc[data,"month"]<10: #to organize by water year 1 Oct - 30 Sep
        psorted[data,0]=pin.loc[data,"year"]-1
    else:
        psorted[data,0]=pin.loc[data,"year"]
    psorted[data,2]=pin.loc[data,"precip_mm"]
    psorted[data,3]=pin.loc[data,"tmin_C"]
    psorted[data,4]=pin.loc[data,"tmax_C"]

print(psorted)
print(qsorted)

"""Question 1: Calculate the annual runoff ratio for the Cowichan watershed for
each year in a selected 10-year period (to clarify: select 10 years with data 
for both streamflow and precipitation, calculate 10 runoff ratios). 
Plot the time series of the runoff ratios and discuss how they vary 
interannually (Hint: use some statistics to back up your answer!)"""
 
"""Question 2: Calculate monthly runoff ratios for two years of data. How do 
they vary intraannually (within a year) and interannually (across years, for 
example how do the two January runoff ratios compare)?"""
 
"""Question 3: Calculate and plot a monthly water budget for two years of data.
Discuss how the seasonality of the water budget varies across variables, the 
intra- and interannual variability, and the sources of uncertainty in the water
budget."""
   