#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:10:23 2020

@author: Joseph Martin, University of Victoria
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Sort the dataframes first into useable matrices!!"""

pin=pd.read_csv("/home/josmarti/Code/CIVE-580/Assignment1/1022571_Duncan_Glenora.csv")
qin=pd.read_csv("Cowichan_Duncan_monthlyQ.csv")
psorted=pd.DataFrame(columns = ["water year", "month", "precip_mm", "tmin_C", "tmax_C"])
qsorted=pd.DataFrame(columns = ["water year", "month", "Q_mms"])

for data in range(len(qin["Unnamed: 0"])):
    qsorted.loc[data,"month"]=int(qin.loc[data,"Unnamed: 0"][5:7]) #making months useable integers
    if int(qin.loc[data,"Unnamed: 0"][5:7])<10: #to organize by water year 1 Oct - 30 Sep
        qsorted.loc[data,"water year"]=int(qin.loc[data,"Unnamed: 0"][0:4])-1 #making years useable integers
    else:
        qsorted.loc[data,"water year"]=int(qin.loc[data,"Unnamed: 0"][0:4]) #making years useable integers
    qsorted.loc[data,"Q_mms"]=qin.loc[data,"Q_cms"]*10

for data in range(len(pin["Unnamed: 0"])):
    psorted.loc[data,"month"]=pin.loc[data,"month"] #no int() needed as the values in this dataframe are already integers
    if pin.loc[data,"month"]<10: #to organize by water year 1 Oct - 30 Sep
        psorted.loc[data,"water year"]=pin.loc[data,"year"]-1
    else:
        psorted.loc[data,"water year"]=pin.loc[data,"year"]
    psorted.loc[data,"precip_mm"]=pin.loc[data,"precip_mm"]
    psorted.loc[data,"tmin_C"]=pin.loc[data,"tmin_C"]
    psorted.loc[data,"tmax_C"]=pin.loc[data,"tmax_C"]


df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=['year', 'precip_mm', 'tmin_C'])

#print(psorted)
#print(qsorted)

"""Question 1: Calculate the annual runoff ratio for the Cowichan watershed for
each year in a selected 10-year period (to clarify: select 10 years with data 
for both streamflow and precipitation, calculate 10 runoff ratios). 
Plot the time series of the runoff ratios and discuss how they vary 
interannually (Hint: use some statistics to back up your answer!)"""

timeframe1=range(1994,2004) #due to zero indexing, the end year is not included
arratio=pd.Series(index=timeframe1)
annualp=psorted["precip_mm"].where(psorted["water year"]==1994)

#print(qsorted.where["water year"==1994, "Q_cms"])



for year in timeframe1:
    annualp=psorted["precip_mm"].where(psorted["water year"]==year)
    annualq=qsorted["Q_mms"].where(qsorted["water year"]==year)
    arratio[year]=annualq.mean()/annualp.mean()

print(arratio)

arratio.plot(kind='bar',rot=0)
plt.xlabel("Water Years")	
plt.ylabel("Runoff ratio")
plt.title("Runoff Ratios for Duncan Glenora from %s " % str(np.amin(timeframe1)) + "to %s" % str(np.amax(timeframe1)))
plt.show()
#title=() )

 
"""Question 2: Calculate monthly runoff ratios for two years of data. How do 
they vary intraannually (within a year) and interannually (across years, for 
example how do the two January runoff ratios compare)?"""

months=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

timeframe2=range(2006, 2008) #due to zero indexing, the end year is not included
rryears=range(len(timeframe2))+np.amin(timeframe2)
for i in range(len(rryears)): #convert time frame years into str for DataFrame columns
    rryears[i]=str(rryears[i])
mrratio=pd.DataFrame(columns=rryears, index=months)
for m in months:
    for year in rryears:
        monthlyp=psorted["precip_mm"].where((psorted["water year"]==int(year)) & (psorted["month"]==(months.index(m)+1)))
        monthlyq=qsorted["Q_mms"].where((qsorted["water year"]==int(year)) & (qsorted["month"]==(months.index(m)+1)))
        mrratio.loc[m, year]=monthlyq.mean()/monthlyp.mean() #there must be a better way...
print(mrratio)

mrratio.plot(kind='bar',rot=0)
plt.xlabel("Months")	
plt.ylabel("Runoff ratio")
plt.title("Runoff Ratios for Duncan Glenora from %s " % str(np.amin(timeframe2)) + "to %s" % str(np.amax(timeframe2)))
plt.show()
                        
                        
"""Question 3: Calculate and plot a monthly water budget for two years of data.
Discuss how the seasonality of the water budget varies across variables, the 
intra- and interannual variability, and the sources of uncertainty in the water
budget."""

ETin=pd.read_csv("North_Cowichan_ET_2005-2008.csv")
print(ETin)
