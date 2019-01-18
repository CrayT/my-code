import random
import math
import csv
import operator
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler #[0,1]
mm=MinMaxScaler()
def loadDataset(filename,split,train=[],test = []):    
    with open(filename,"rb") as csvfile:    
        lines = csv.reader(csvfile)    
        dataset = list(lines) 
        dataset=mm.fit_transform(dataset)   
        #print dataset
        for x in range(len(dataset)-1):    
            for y in range(3):    
                dataset[x][y] = float(dataset[x][y])    
            if random.random()<split:    
                train.append(dataset[x])    
            else:    
                test.append(dataset[x])
        #print train[0][0]  
    #train=mm.fit_transform(train)  
    #test=mm.fit_transform(test)
    #print test
def euDistance(sample1,sample2,length):
    distance=0
    for x in range(length):
        #print sample1[x],sample2[x]
        distance +=pow((float(sample1[x])-float(sample2[x])),2)
        #print distance
    return distance
def Neighbors(train,test,k):
    distances=[]
    length=len(test)-1 
    #print len(train)
    for x in range(len(train)):
        dist=euDistance(test,train[x],length)
        distances.append((train[x],dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors=[]
    for x in range(2):
       # print neighbors
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes={}
    for x in range(len(neighbors)):
        response=neighbors[x][0]
        if response in classVotes:
            classVotes[response]+=1
        else:
            classVotes[response]=1
    sortVotes=sorted(classVotes.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortVotes[0][0]

def Accuracy(test,predict):
    correct=0
    for x in range(len(test)):
        #print len(test)
        if test[x][0]==predict[x]:
            correct+=1
        #print correct
    return (correct/float(len(test)))*1.0
