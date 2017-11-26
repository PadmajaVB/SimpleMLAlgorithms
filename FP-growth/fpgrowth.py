class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      
        self.children = {} 
           
    def inc(self, numOccur):
        self.count += numOccur
        
#displays tree       
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)
            
def createTree(dataSet, minSup=1): #create FP-tree from dataset but doesn't mine
    headerTable = {}
    #goes dataSet twice
    for trans in dataSet: # first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + 1
    #print("HT=",dataSet)        
    for k in list(headerTable):  # remove items not meeting minSup
        if headerTable[k] < minSup: 
            del(headerTable[k])
    print("HeaderTable",headerTable)        
    freqItemSet = set(headerTable.keys())
    #print 'freqItemSet: ',freqItemSet
    
    if len(freqItemSet) == 0: return None, None  # if no items meet min support -->exit
    
    for k in headerTable:
        headerTable[k] = [headerTable[k], None] # reformat headerTable to use Node link 
    #print('headerTable: ',headerTable)
    retTree = treeNode('Null Set', 1, None) # create tree
    
    for tranSet, count in dataSet.items():  # go through dataset 2nd time to build the order table
        localD = {}
        for item in tranSet:  # put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count) # populate tree with ordered freq itemset
    return retTree, headerTable # return tree and header table
    
def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children: # check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) # incrament count
    else:   # add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: # update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1: # call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(nodeToTest, targetNode):   
    while (nodeToTest.nodeLink != None):    
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat            

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict
    
def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
        
def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats
    
simpDat = loadSimpDat()
initSet = createInitSet(simpDat)
#The FP-tree
myFPtree, myHeaderTab = createTree(initSet, 3)
myFPtree.disp()

print("-----Fixed path--------")
print("From x:",findPrefixPath('x', myHeaderTab['x'][1]))
print("From r:",findPrefixPath('r', myHeaderTab['r'][1]))
                                
