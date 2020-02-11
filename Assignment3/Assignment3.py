import pandas as pd

up=pd.read_csv("River_routing_data.csv")

time_min=12
timestep=[]
j=0
while j<(60/time_min):
	timestep.append(time_min*j)
	j+=1

print (timestep)
q=pd.DataFrame(0, index=range(len(up)*len(timestep)-(len(timestep)-1)), columns=["YEAR", "MONTH", "DAY", "HOUR","MINUTES","Qup_cfs","Qdown_cfs"])
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

print (q)

dist_ft=100*2
Length=5280*10
diststep=[]
k=0
while dist_ft*k<=Length:
	diststep.append(dist_ft*k)
	k+=1
print (diststep)

qroute=pd.DataFrame(0, index=range(len(q)), columns=diststep)

qroute.iloc[0,:]=q.iloc[0,5] #set initial conditions
qroute.iloc[:,0]=q.iloc[:,5]
step=(time_min*60)/dist_ft
alpha=2.49 #temp
beta=0.6 #confirm

print(qroute.iloc[1,0])
print(step+alpha*beta*((qroute.iloc[0,1]+qroute.iloc[1,0])/2)**(0.6-1))

for j in range(len(q)-1):
	for i in range(len(diststep)-1):
		num=step*qroute.iloc[(j+1),i]+alpha*beta*qroute.iloc[j,(i+1)]*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1)
		print(qroute.iloc[j,(i+1)])
		print(qroute.iloc[(j+1),i])
		print(num)
		denom=step+alpha*beta*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1)
		print(denom)
		print(num/denom)
		qroute.iloc[(j+1),(i+1)]=(step*qroute.iloc[(j+1),i]+alpha*beta*qroute.iloc[j,(i+1)]*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))/(step+alpha*beta*((qroute.iloc[j,(i+1)]+qroute.iloc[(j+1),i])/2)**(0.6-1))

print(qroute)
