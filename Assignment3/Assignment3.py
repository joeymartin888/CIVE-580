import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as fig
import matplotlib.dates as mdates

up=pd.read_csv("River_routing_data.csv")

"""Question 1: Route the streamflow from Walnutport to Whitehall, ensuring the 
Courant condition is met."""

time_min=3 #Change timestep as required to meet Courant condition
timestep=[]
j=0
while j<(60/time_min):
	timestep.append(time_min*j)
	j+=1

#print (timestep)
q=pd.DataFrame(0, index=range(len(up)*len(timestep)-(len(timestep)-1)), columns=["YEAR", "MONTH", "DAY", "HOUR","MINUTE","Walnutport","Whitehall"])
for i in range(len(up)):
	for t in range(len(timestep)):
		q.iloc[(i*len(timestep)+t),0]=up.iloc[i,0]
		q.iloc[(i*len(timestep)+t),1]=up.iloc[i,1]
		q.iloc[(i*len(timestep)+t),2]=up.iloc[i,2]
		q.iloc[(i*len(timestep)+t),3]=up.iloc[i,3]
		q.iloc[(i*len(timestep)+t),4]=timestep[t]
		if i==(len(up)-1):
			q.iloc[(i*len(timestep)+t),5]=up.iloc[i,4]
			break
		q.iloc[(i*len(timestep)+t),5]=((up.iloc[i+1,4]-up.iloc[i,4])*t)/(len(timestep))+up.iloc[i,4]

#print (q)

dist_ft=5280/4
Length=5280*10
diststep=[]
k=0
while dist_ft*k<=Length:
	diststep.append(dist_ft*k)
	k+=1
#print (diststep)

qroute=pd.DataFrame(0, index=range(len(q)), columns=diststep)

qroute.iloc[0,:]=q.iloc[0,5] #set initial conditions
qroute.iloc[:,0]=q.iloc[:,5]
step=(time_min*60.0)/dist_ft
#print(step)
alpha=4.13 #temp
beta=0.6 #confirm

#print(qroute.iloc[1,0])
#print(step+alpha*beta*((qroute.iloc[0,1]+qroute.iloc[1,0])/2)**(0.6-1))

for j in range(len(q)-1):
	for i in range(len(diststep)-1):
		num=step*qroute.iloc[(j+1),i]+alpha*beta*qroute.iloc[j,(i+1)]*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1)
		denom=step+alpha*beta*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1)
		qroute.iloc[(j+1),(i+1)]=(step*qroute.iloc[(j+1),i]+alpha*beta*qroute.iloc[j,(i+1)]*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))/(step+alpha*beta*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))

#print(qroute)

q["Whitehall"]=qroute.iloc[:,(len(qroute.columns)-1)]

"""Question 2: Plot the upstream and downstream hydrographs on the same plot."""


newq=pd.DataFrame(columns=["Time", "Walnutport","Whitehall"])
newq["Time"]=pd.to_datetime(q.iloc[:,0:5])
newq["Walnutport"]=q["Walnutport"]
newq["Whitehall"]=q["Whitehall"]


x=pd.to_datetime(q.iloc[:,0:5])
fig, ax = plt.subplots()
ax.plot(newq["Time"], newq["Walnutport"])
ax.plot(newq["Time"], newq["Whitehall"])
plt.xlabel("Time (Day and Hour) - timestep = %i min" % time_min)	
fig.autofmt_xdate(bottom=None, rotation=30)
#ax.fmt_xdata = mdates.DateFormatter('%d')
plt.ylabel("Streamflow (in cfs)")
plt.title("Stream Routing of Lehigh River from Walnutport to Whitehall")
plt.legend()
plt.show()

"""Question 3: What is the speed of the flood wave? You may approximate
this with the time between the two peaks of the hydrographs."""

flood_up=newq["Time"].where(newq["Walnutport"]==max(newq["Walnutport"]))
flood_down=newq["Time"].where(newq["Whitehall"]==max(newq["Whitehall"]))
f=flood_down.dropna()
g=flood_up.dropna()
flood_time=f.iloc[0]-g.iloc[0]
j=flood_time.seconds
flood_speed=Length/flood_time.seconds
print("The flood wave travelled at %0.2f cfs." % flood_speed)