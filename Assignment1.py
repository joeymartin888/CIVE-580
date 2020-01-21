import unicodedata
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
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


