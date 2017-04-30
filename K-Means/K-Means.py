import csv
from collections import defaultdict
from collections import Counter
import random
import math
n=110
k=2

def loadCsv(filename):
	lines=csv.reader(open(filename,'r'))
	dataset=list(lines)
	for i in range(len(dataset)):
		dataset[i]=[float(x) for x in dataset[i]]
	return dataset	
	
def findCluster(dataset, Array):
	Cluster=[]
	distance=[]
	dist=0
	
	for i in range(len(dataset)):
		distance.append([])
		for p in range(len(Array)):
			dist=0
			for j in range(len(dataset[i])-1):
				data=Array[p][j]
				dist+=math.pow((dataset[i][j]-data),2) 
			distance[i].append(math.sqrt(dist)) 
		c=min(distance[i])
		Cluster.append(distance[i].index(c))
	return Cluster		
	
def SeperateByCluster(dataset,Cluster):
	seperated={}
	for i in range(len(dataset)):
		vector=dataset[i]
		if(Cluster[i] not in seperated):
			seperated[Cluster[i]]=[]
		seperated[Cluster[i]].append(vector)
	return seperated
		
def mean(numbers):
	return sum(numbers)/float(len(numbers))	
	
def findMean(instances):
	meanVal=[mean(attribute) for attribute in zip(*instances)]	
	del meanVal[-1]
	return meanVal
	
def NewCentroid(dataset,Cluster):	
	seperated=SeperateByCluster(dataset,Cluster)
	
	meanValue={}
	for cluster, instances in seperated.items():
		meanValue[cluster]=findMean(instances)
		
	return meanValue
	
def CalculateAccuracy(cluster,dataset):	
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
	filename='SPECTF_New.csv'	
	dataset=loadCsv(filename)
	Random=[random.randint(0,len(dataset)-1) for x in range(k)]
	RandomArray=[]
	for i in range(len(Random)):
		RandomArray.append([])
		for j in range(0,len(dataset[i])):
			RandomArray[i].append(dataset[Random[i]][j]) 		
			
	Cluster=findCluster(dataset,RandomArray)
	SetofCentroids=[]
	SetofCentroids.append(RandomArray)
	
	for i in range(1,21):
		centroid=NewCentroid(dataset,Cluster)
		Cluster=findCluster(dataset,centroid)
		SetofCentroids.append(centroid)
		if(SetofCentroids[i]==SetofCentroids[i-1]):
			break
			
	print('iterations=',i+1)				
	print('Clusters=',Cluster)
	print('Centroid=',centroid)		
	print()
	CalculateAccuracy(Cluster,dataset)
	
main()	

