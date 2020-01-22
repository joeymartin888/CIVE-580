# CIVE 580 - Assignment 1

import matplotlib.pyplot as plt
import pandas as pd

#1. Calculate the seasonal cycle of precipitation and temperature 
#(P and T, respectively) for both stations. The seasonal cycle 
#would be averaging all January months together, then all February, 
#etc. How do the seasonal cycles compare across stations? (Hint: a 
#figure would be very useful to answer this question).


cov=[0 for g in range(12)]
psum=[0 for i in range(12)]
means=[0 for i in range(12)]
jump=pd.read_csv("3B23P_Jump_Creek.csv") #load in csvs
duncan=pd.read_csv("1022571_Duncan_Glenora.csv")
months=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
conditions=["tmax_C","tmin_C","precip_mm"] 
print("3B23P_Jump_Creek.csv")
for t in conditions: # loop through conditions
	print(t)
	for x in range(0, 12): # loop through monthd
		temp=jump[t].where(jump['month']==(x+1)) # python zero-index
		temp.dropna() #remove NaNs
		means[x]=temp.mean()
	print(means)
	tp=pd.Series(means, index=months)
	tp.plot(kind='bar',rot=0)
	plt.xlabel("Months")	
	if t=="precip_mm":
		plt.ylabel("Precipitation in mm")
		tp.plot(title="Average Precipitation Monthly for Jump Creek")
	else:
		plt.ylabel("Temperature in degrees Celsius")
		if t=="tmax_C":
			tp.plot(title="Maximum Monthly Temperatures for Jump Creek")
		else:
			tp.plot(title="Minimum Monthly Temperatures for Jump Creek")	
	plt.show()

print("1022571_Duncan_Glenora.csv")
for t in conditions: # loop through conditions
	print(t)
	for x in range(0, 12): # loop through monthd
		temp=duncan[t].where(duncan['month']==(x+1)) # python zero-index
		temp.dropna() #remove NaNs
		means[x]=temp.mean()
	print(means)
	p=pd.Series(means, index=months)
	tp.plot(kind='bar',rot=0)
	plt.xlabel("Months")	
	if t=="precip_mm":
		plt.ylabel("Precipitation in mm")
		tp.plot(title="Average Precipitation Monthly for Duncan Glenora")
	else:
		plt.ylabel("Temperature in degrees Celsius")
		if t=="tmax_C":
			tp.plot(title="Maximum Monthly Temperatures for Duncan Glenora")
		else:
			tp.plot(title="Minimum Monthly Temperatures for Duncan Glenora")	
	plt.show()

#2. Calculate the coefficient of variability for annual precipitation for each 
#station. How do they compare?
    
    
print("3B23P_Jump_Creek.csv")
for x in range(1996, 2008): # loop through monthd
	temp=jump['precip_mm'].where(jump['year']==(x)) # python zero-index
	temp.dropna() #remove NaNs
	psum[x-1996]=temp.sum()
	jsum=pd.Series(psum, index=range(1996, 2008))
print(jsum)
jcov=jsum.mean()/jsum.std()
print(jcov)

print("1022571_Duncan_Glenora.csv")
for x in range(1996, 2008): # loop through monthd
	temp=duncan['precip_mm'].where(duncan['year']==(x)) # python zero-index
	temp.dropna() #remove NaNs
	psum[x-1996]=temp.sum()
	dsum=pd.Series(psum, index=range(1996, 2008))
print(dsum)
dcov=dsum.mean()/dsum.std()
print(dcov)


#3. Using your answers above and your understanding of the water budget 
#equation from our first week of class (ds/dt = P-ET-streamflow), how important 
#is snowfall and the seasonal snowpack in this basin?

print("3B23P_Jump_Creek.csv")

snowj=jump['precip_mm'].where(((jump['tmin_C']+jump['tmax_C'])/2)<0) #avg<0
totalj=jump['precip_mm']
snowpercentj=snowj.sum()/totalj.sum()
print(snowpercentj)


snowminj=jump['precip_mm'].where(jump['tmin_C']<0) #min<0
totalj=jump['precip_mm']
snowminpercentj=snowminj.sum()/totalj.sum()
print(snowminpercentj)

print("1022571_Duncan_Glenora.csv")

snowd=duncan['precip_mm'].where(((duncan['tmin_C']+jump['tmax_C'])/2)<0) #avg<0
totald=duncan['precip_mm']
snowpercentd=snowd.sum()/totald.sum()
print(snowpercentd)


snowmind=duncan['precip_mm'].where(duncan['tmin_C']<0) #min<0
totald=duncan['precip_mm']
snowminpercentd=snowmind.sum()/totald.sum()
print(snowminpercentd)
