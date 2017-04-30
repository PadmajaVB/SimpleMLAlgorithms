import csv
import random
from random import randrange
import math

def loadCsv(C, filename):
	lines = csv.reader(open(filename, 'r'))
	dataset = list(lines)
	finaldataset=[]
	for i in range(len(dataset)):
		finaldataset.append([])
		for j in range(len(dataset[i])-1):
			if(C[j]==1):
				data=float(dataset[i][j])
				finaldataset[i].append(data)
		finaldataset[i].append(float(dataset[i][-1]))	
	return finaldataset	
	
def splitDataset(dataset, splitRatio):
	trainSize=int(len(dataset)*splitRatio)
	trainSet=[]	
	copy=list(dataset)
	while(len(trainSet)<trainSize):
		index=random.randrange(len(copy))
		trainSet.append(copy.pop(index))
	testSet=copy	
	return [trainSet, testSet]	
	
def seperatedByClass(dataset):
	seperated={}
	for i in range(len(dataset)):
		vector=dataset[i]
		if(vector[-1] not in seperated):
			seperated[vector[-1]]=[]
		seperated[vector[-1]].append(vector)
	return seperated			
	
def mean(numbers):
	return sum(numbers)/float(len(numbers))
	
def stdev(numbers):
	avg=mean(numbers)
	variance=sum([pow(x-avg, 2) for x in numbers])/float(len(numbers)-1)
	return math.sqrt(variance)
	
def summarize(dataset):
	summaries=[(mean(attribute), stdev(attribute)) for attribute in zip(*dataset)]
	del summaries[-1]
	return summaries
	
def summarizeByClass(dataset):
	seperated=seperatedByClass(dataset)
	summaries={}
	for classValue, instances in seperated.items():
		summaries[classValue]=summarize(instances)
	return summaries
	
def calculateProbability(x, mean, stdev):
	if(stdev==0):
		stdev=random.uniform(0,3)
	exponent=math.exp(-(math.pow(x-mean,2)/float(2*math.pow(stdev,2))))
	return (1/(math.sqrt(2*math.pi)*stdev)) * exponent
	
def calculateClassProbabilities(summaries, inputVector):
	probabilities = {}
	for classValue, classSummaries in summaries.items():
		probabilities[classValue]=1
		for i in range(len(classSummaries)):
			mean, stdev=classSummaries[i]
			x=inputVector[i]
			probabilities[classValue]*=calculateProbability(x, mean, stdev)
	return probabilities
	
def predict(summaries, inputVector):
	probabilities=calculateClassProbabilities(summaries, inputVector)
	bestLabel, bestProb=None, -1
	for classValue, probability in probabilities.items():
		if bestLabel is None or probability > bestProb:
			bestProb = probability
			bestLabel = classValue
	return bestLabel
	
def getPredictions(summaries, testSet):
	predictions=[]
	for i in range(len(testSet)):
		result=predict(summaries,testSet[i])
		predictions.append(result)
	return predictions
					 						
def getAccuracy(testSet, predictions):
	correct=0
	for i in range(len(testSet)):
		if testSet[i][-1] == predictions[i]:
			correct += 1
	return (correct/float(len(testSet))) * 100.0

# Split a dataset into k folds
def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	fold_size = int(len(dataset) / n_folds)
	for i in range(n_folds):
		fold = list()
		while len(fold) < fold_size:
			index = randrange(len(dataset_copy))
			fold.append(dataset_copy.pop(index))
		dataset_split.append(fold)
	return dataset_split
	
def main(C):
	filename='Glass_New.csv'
	#splitRatio=0.67
	dataset=loadCsv(C,filename)
	n_folds = 10
	folds = cross_validation_split(dataset, n_folds)
	scores = list()
	for fold in folds:
		trainSet = list(folds)
		trainSet.remove(fold)
		trainSet = sum(trainSet, [])
		testSet = list()
		for row in fold:
			row_copy = list(row)
			testSet.append(row_copy)
	
		#trainingSet, testSet = splitDataset(dataset, splitRatio)
		#print('trainSet[0]=',trainSet[0])
		#print('testSet[0]=',testSet[0])
		#prepare model
		summaries = summarizeByClass(trainSet)
	
		#test model
		predictions=getPredictions(summaries, testSet)
		accuracy = getAccuracy(testSet, predictions)
		scores.append(accuracy)

	return accuracy

#main()				

				
