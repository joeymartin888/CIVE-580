#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:10:23 2020

@author: Joseph Martin, University of Victoria
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

"""Data sorting"""
qinf=pd.read_csv("Cowichan_Duncan_dailyQ.csv")

pin1=pd.read_csv("/home/josmarti/Code/CIVE-580/Assignment1/3B23P_Jump_Creek.csv")
pin2=pd.read_csv("/home/josmarti/Code/CIVE-580/Assignment1/1022571_Duncan_Glenora.csv")
qin=pd.read_csv("Cowichan_Duncan_monthlyQ.csv")
psorted=pd.DataFrame(columns = ["water year", "month", "precip_mm", "tmin_C", "tmax_C"])
qdailysorted=pd.DataFrame(columns = ["water year", "month", "Q_mms"])
qsorted=pd.DataFrame(columns = ["water year", "month", "Q_mms"])

for data in range(len(qinf["Unnamed: 0"])):
    qdailysorted.loc[data,"month"]=int(qinf.loc[data,"Unnamed: 0"][5:7]) #making months useable integers
    if int(qinf.loc[data,"Unnamed: 0"][5:7])<10: #to organize by water year 1 Oct - 30 Sep
        qdailysorted.loc[data,"water year"]=int(qinf.loc[data,"Unnamed: 0"][0:4])-1 #making years useable integers
    else:
        qdailysorted.loc[data,"water year"]=int(qinf.loc[data,"Unnamed: 0"][0:4]) #making years useable integers
    qdailysorted.loc[data,"Q_mms"]=qinf.loc[data,"Q_cms"]*10

j=0 #not pretty, but the best case in a pinch...
for year in range(np.amin(qdailysorted["water year"]),np.amax(qdailysorted["water year"])):
    for month in range (np.amin(qdailysorted["month"]),(np.amax(qdailysorted["month"])+1)):
        temp=qdailysorted["Q_mms"].where((qdailysorted["water year"]==year) & (qdailysorted["month"]==month))
        qsorted.loc[j,"water year"]=year
        qsorted.loc[j,"month"]=month
        qsorted.loc[j,"Q_mms"]=temp.mean()
        j=j+1


for data in range(len(pin1["Unnamed: 0"])):
    psorted.loc[data,"month"]=pin1.loc[data,"month"] #no int() needed as the values in this dataframe are already integers
    if pin1.loc[data,"month"]<10: #to organize by water year 1 Oct - 30 Sep
        psorted.loc[data,"water year"]=pin1.loc[data,"year"]-1
    else:
        psorted.loc[data,"water year"]=pin1.loc[data,"year"]
    grabp2=pin2["precip_mm"].where((pin2["year"]==pin1.loc[data,"year"])&(pin2["month"]==pin1.loc[data,"month"]))
    psorted.loc[data,"precip_mm"]=pin1.loc[data,"precip_mm"]+grabp2.mean() #both stations contribute to watershed
    psorted.loc[data,"tmin_C"]=pin1.loc[data,"tmin_C"]
    psorted.loc[data,"tmax_C"]=pin1.loc[data,"tmax_C"]
    



df2 = pd.DataFrame(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
                   columns=['year', 'precip_mm', 'tmin_C'])

#print(psorted)
#print(qsorted)

"""Question 1: Calculate the annual runoff ratio for the Cowichan watershed for
each year in a selected 10-year period (to clarify: select 10 years with data 
for both streamflow and precipitation, calculate 10 runoff ratios). 
Plot the time series of the runoff ratios and discuss how they vary 
interannually (Hint: use some statistics to back up your answer!)"""

timeframe1=range(1997,2007) #due to zero indexing, the end year is not included
arratio=pd.Series(index=timeframe1)

#print(qsorted.where["water year"==1994, "Q_cms"])


for year in timeframe1:
    annualp=psorted["precip_mm"].where(psorted["water year"]==year)
    annualq=qsorted["Q_mms"].where(qsorted["water year"]==year)
    arratio[year]=annualq.mean()/annualp.mean()

#print(arratio)
arratio.plot(kind='bar',rot=0)
plt.xlabel("Water Years")	
plt.ylabel("Runoff ratio")
plt.title("Annual Runoff Ratios for Duncan Glenora from %s " % str(np.amin(timeframe1)) + "to %s" % str(np.amax(timeframe1)))
plt.show()
#title=() )

print("Annual Variability Coefficient is: %0.3f" % (arratio.std()/arratio.mean()))

"""Question 2: Calculate monthly runoff ratios for two years of data. How do 
they vary intraannually (within a year) and interannually (across years, for 
example how do the two January runoff ratios compare)?"""

months=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

timeframe2=range(2005, 2007) #due to zero indexing, the end year is not included
rryears=range(len(timeframe2))+np.amin(timeframe2)
for i in range(len(rryears)): #convert time frame years into str for DataFrame columns
    rryears[i]=str(rryears[i])
mrratio=pd.DataFrame(columns=rryears, index=months)
for m in months:
    for year in rryears:
        monthlyp=psorted["precip_mm"].where((psorted["water year"]==int(year)) & (psorted["month"]==(months.index(m)+1)))
        monthlyq=qsorted["Q_mms"].where((qsorted["water year"]==int(year)) & (qsorted["month"]==(months.index(m)+1)))
        mrratio.loc[m, year]=monthlyq.mean()/monthlyp.mean() #there must be a better way...
#print(mrratio)

mrratio.plot(kind='bar',rot=0)
plt.xlabel("Months")	
plt.ylabel("Runoff ratio")
plt.title("Monthly Runoff Ratios for Duncan Glenora from %s " % str(np.amin(timeframe2)) + "to %s" % str(np.amax(timeframe2)))
plt.show()

for year in rryears:
    var=mrratio[year]
    print("Annual Variability Coefficient for %i" % year + " is %0.3f" % (var.std()/var.mean()))


for month in months:
    var=mrratio.loc[month]
    print("Monthly Variability for %s" % month + " is: %0.3f" % (var.std()/var.mean()))                        
   
               
"""Question 3: Calculate and plot a monthly water budget for two years of data.
Discuss how the seasonality of the water budget varies across variables, the 
intra- and interannual variability, and the sources of uncertainty in the water
budget."""

ETin=pd.read_csv("North_Cowichan_ET_2005-2008.csv")
ETsorted=pd.DataFrame(columns = ["water year", "month", "ET_mm"], index=months)

for data in range(len(ETin["Date"])):
    ETsorted.loc[data,"month"]=int(ETin.loc[data,"Date"][5:7]) #making months useable integers
    if int(ETin.loc[data,"Date"][5:7])<10: #to organize by water year 1 Oct - 30 Sep
        ETsorted.loc[data,"water year"]=int(ETin.loc[data,"Date"][0:4])-1 #making years useable integers
    else:
        ETsorted.loc[data,"water year"]=int(ETin.loc[data,"Date"][0:4]) #making years useable integers
    ETsorted.loc[data,"ET_mm"]=ETin.loc[data,"ET"]

timeframe3=range(2005, 2007) #due to zero indexing, the end year is not included
rryears2=range(len(timeframe3))+np.amin(timeframe3)
for i in range(len(rryears2)): #convert time frame years into str for DataFrame columns
    rryears2[i]=str(rryears2[i])
budget=pd.DataFrame(columns=rryears2, index=months)
for m in months:
    for year in rryears2:
        budgetp=psorted["precip_mm"].where((psorted["water year"]==int(year)) & (psorted["month"]==(months.index(m)+1)))
        budgetq=qsorted["Q_mms"].where((qsorted["water year"]==int(year)) & (qsorted["month"]==(months.index(m)+1)))
	budgetET=ETsorted["ET_mm"].where((ETsorted["water year"]==int(year)) & (ETsorted["month"]==(months.index(m)+1)))
	#print(budgetET.sum())
	budget.loc[m, year]=budgetp.mean()-budgetq.mean()-budgetET.sum()

budget.plot(kind='bar',rot=0)
plt.xlabel("Months")	
plt.ylabel("Water Budget in mm (dS/dt)")
plt.title("Montly Water Budget for Duncan Glenora from %s " % str(np.amin(timeframe3)) + "to %s" % str(np.amax(timeframe3)))
plt.show()

for year in rryears2:
    var=budget[year]
    print("Annual Variability Coefficient for %i" % year + " is %0.3f" % (var.std()/var.mean()))


for month in months:
    var=budget.loc[month]
    print("Monthly Variability for %s" % month + " is: %0.3f" % (var.std()/var.mean()))    