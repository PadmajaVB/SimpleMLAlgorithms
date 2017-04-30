import random
import NaiveBayes

population_size=30 # Total number of chromosome
chromLength=9 # Represents the number of attributes in the dataset except the class label
CrossoverRate=0.25
MutationRate=0.10

#This function randomly initializes each chromosome
def initializeChromosome():
	C=[]
	for i in range(population_size):
		C.append([])
		for x in range(chromLength):
			C[i].append(random.randint(0,1))
	return C	

#This function calculates the fitness of each chromosome
def calculateFitness(C, algorithm):
	F=[]
	for i in range(population_size):
		F.append(algorithm.main(C[i]))
	#print('Fitness=',F,' len=',len(F))	
				
	return F

#This function selects chromosome from the population based on Roulette Wheel selection 	
def RouletteWheel(F):
	total=sum(F)
	probability=[x/float(total) for x in F]
	CProb=0
	CumProbability=[]
	for p in probability:
		CProb+=p
		CumProbability.append(CProb)
		
	randomArray=[random.uniform(0,1) for i in range(population_size)]	
	
	selected=[]
	for i in range(len(randomArray)):
		for j in range(len(CumProbability)):
			if(randomArray[i]<CumProbability[j]):
				selected.append(j)
				break
	
	#print('prob=',probability)
	#print('cprob=',CumProbability)
	#print ('selected=',selected)
	return selected
		
#This function updates the population based on the selected chromoses		
def updatePopulation(selected, C):
	copy=C
	C=[copy[x] for x in selected]	
	return C
	
#CrossOver and Mutation is done in order to avoid Elitism 	
def CrossOver(UpdatedC):
	randomArray=[random.uniform(0,1) for i in range(population_size)]
	
	selected=[]
	copy=UpdatedC
	
	for i in range(len(randomArray)):
		if(randomArray[i]<CrossoverRate):
			selected.append(i)
	#print('Selected=',selected)
	#print('BeforeUpdate=',UpdatedC)
	COSection=chromLength-1
	RandomSection=[random.randint(1,COSection) for i in range(len(selected))]
	#print('RandomSection=',RandomSection)
	
	for i in range(len(selected)):
		a=copy[selected[i]]
		
		if(i==(len(selected)-1)):
			b=copy[selected[0]]
		else:	
			b=copy[selected[i+1]]
		
		for j in range(RandomSection[i],len(a)):
			a[j]=b[j]
		UpdatedC[i]=a
	#print('UpdatedC=',UpdatedC)
	return UpdatedC			
	
def Mutation(Chromosome):
	genes=population_size * chromLength
	mutate=int(genes * MutationRate)
	randomArray=[random.randint(0,genes-1) for i in range(mutate)]
	#print ('mutate=',randomArray)
	#print('BeforeUpdate=',Chromosome)
	for x in randomArray:
		ChromNo=int(x/chromLength)
		gene= x % chromLength
		#print('CNo.=',ChromNo,' gene=',gene)
		if(Chromosome[ChromNo][gene]==0):
			Chromosome[ChromNo][gene]=1
		else:
			Chromosome[ChromNo][gene]=0		
	#print ('Chromosome=',Chromosome)
	return Chromosome
	
def main():	
	C=initializeChromosome()
	
	for i in range(20):
		F=calculateFitness(C, NaiveBayes)
		print('Best Fitness=',max(F), ' Chromosome selected=',C[F.index(max(F))])
		selected=RouletteWheel(F)
		UpdatedC=updatePopulation(selected, C)
		AfterCrossover=CrossOver(UpdatedC)
		Mutated=Mutation(AfterCrossover)
		C=Mutated

main()	



