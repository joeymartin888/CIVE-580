import pandas as pd
import numpy as np
means=[0 for i in range(12)]
jump=pd.read_csv("3B23P_Jump_Creek.csv") #load in csv
conditions=["tmax_C","tmin_C","precip_mm"] 
for t in conditions: # loop through conditions
	print(t)
	for x in range(0, 12): # loop through monthd
		temp=jump[t].where(jump['month']==(x+1)) # python zero-index
		temp.dropna() #remove NaNs
		means[x]=temp.mean()
	print(means)
