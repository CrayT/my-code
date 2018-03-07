#-*- coding: utf-8 -*-  
#version：0.1  
#note:该即用API能查询电话号码基本归属信息（只能查到省份）  
from time import  time
import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
estimator=PCA(n_components=4) #将高维压缩
data=pd.read_csv('/Users/xutao/Desktop/2.csv',header=None)
meanVals=np.mean(data,axis=0)
meanRemove=meanVals-data #去中心化
print "\nZero-centered:"
print meanRemove
covMat=np.cov(meanRemove,rowvar=0)
print "\nCovariance Matrix:"
print covMat
eigVals,eigVects=np.linalg.eig(np.mat(covMat))
print "\neigenvalue :"
print eigVals
print "\neigenvector :"
print eigVects
eigValInd=np.argsort(-eigVals) #降序
print '\neigenvalue after sorted'
print eigValInd
redEigVects=eigVects[:,eigValInd]
print "\neigenvector"
print redEigVects
print "\nfinalData:"
print np.dot(meanRemove,redEigVects)
print data
for i in range(5):
    estimator=PCA(n_components=i)
    start=time()
    data1=estimator.fit_transform(data)
    end=time()
    print i,":"
    print "降维后:\n"
    print data1
    print "\ntime:",str(end-start),"s"