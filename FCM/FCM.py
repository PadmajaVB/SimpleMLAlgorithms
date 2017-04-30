import csv
from collections import defaultdict
from collections import Counter
import random
import math
n=110 #total number of tuples in the dataset
c=2   
m=1.25

def loadCsv(filename):
	lines=csv.reader(open(filename,'r'))
	dataset=list(lines)
	for i in range(len(dataset)):
		dataset[i]=[float(x) for x in dataset[i]]
	return dataset
	
def findDistance(centroid, dataset):
	distance=[]	
	for i in range(len(dataset)):
		distance.append([])
		for p in range(len(centroid)):
			dist=0
			for j in range(len(dataset[i])):
				data=centroid[p][j]
				dist+=math.pow((dataset[i][j]-data),2) 
			distance[i].append(math.sqrt(dist)) 	
	return distance		
	
def findMembershipValue(dist):
	u=[]
	cluster=[]
	power=2/(m-1)
	for i in range(len(dist)):
		u.append([])
		for data in dist[i]:
			u[i].append(1/sum([math.pow((data/x),power) for x in dist[i]]))
		d=max(u[i])
		cluster.append(u[i].index(d))	
	return cluster, u			

def findNewCentroid(x, u):
	centroid=[]
	j=0
	for a in zip(*u):
		centroid.append([])
		for b in zip(*x):
			#print("a=",a)
			#print("b=",b)
			p=sum([math.pow(a[i],m)*b[i] for i in range(len(a))]) 
			q=sum([math.pow(a[i],m) for i in range(len(a))])
			centroid[j].append(p/q)
		j+=1			
	return centroid
	
def SeperateByCluster(dataset,Cluster):
	seperated={}
	for i in range(len(dataset)):
		vector=dataset[i]
		if(Cluster[i] not in seperated):
			seperated[Cluster[i]]=[]
		seperated[Cluster[i]].append(vector)
	return seperated	

def CalculateResultMetric(cluster, dataset):	
	seperated=SeperateByCluster(dataset,cluster)
	cls=[]
	belongingCls=[x[-1] for x in dataset]
	count=Counter(belongingCls)
	OccOfZero=count[0]
	OccOfOne=count[1]
	Sum=0
	
	for cluster, instances in seperated.items():
		cls=[x[-1] for x in instances]
		d = defaultdict(int)
		for i in cls:
    			d[i] += 1
		result = max(d.items(), key=lambda x: x[1])
		maxCls, occurance=result
		accuracy=(occurance/len(instances))*100
		print('Cluster=',cluster,'Datapoints=',len(instances))
		
		Sum+=occurance
		precision=occurance/len(instances)
		
		if(maxCls==0):
			total=OccOfZero
			tn=occurance
			fn=len(instances)-tn
					
		elif(maxCls==1):
			total=OccOfOne
			tp=occurance
			fp=len(instances)-tp
		
		recall=occurance/total	
	print('')	
	avgAcc=(Sum/n)*100
	PositivePre=tp/(tp+fp)
	PositiveRec=tp/(tp+fn)
	NegativePre=tn/(tn+fn)
	NegativeRec=tn/(tn+fp)
	print('Accuracy=',avgAcc)					
	#print('Cluster=',cluster,' Max class value=',maxCls))		
	print('Positive Precision=',PositivePre) #fraction of retrived instances that are relevant 	
	print('Positive Recall=',PositiveRec)	#fraction of relevant instnces that are retrived
	print('Negative Precision=',NegativePre)
	print('Negative Recall=',NegativeRec)
	print('')
	
def main():
	filename='SPECTF_cluster.csv'
	sol='SPECTF_New.csv'	
	dataset=loadCsv(filename)
	verify=loadCsv(sol)	
	RandomCentroid=[]
	SetofMemVal=[]
	
	for i in range(c):
		RandomCentroid.append([random.randint(10,90) for x in range(44)])
			
	dist=findDistance(RandomCentroid,dataset)
	cluster, membershipVal=findMembershipValue(dist)
	centroid=findNewCentroid(dataset,membershipVal)
	SetofMemVal.append(membershipVal)
	
	for i in range(1,101):
		dist=findDistance(centroid,dataset)
		cluster, membershipVal=findMembershipValue(dist)
		SetofMemVal.append(membershipVal)
		centroid=findNewCentroid(dataset,membershipVal)
		if(SetofMemVal[i]==SetofMemVal[i-1]):
			break
		if(abs(membershipVal[i][0]-membershipVal[i][1])<0.05):
			break
			
	print('iterations=',i+1)
	print('Clusters=',cluster)				
	#print('Centroid=',centroid)		
	print()	
	CalculateResultMetric(cluster, verify)
	
		
main()	
