#--coding:utf-8--
import re
import lxml
import pandas as pd
import time 
from bs4 import BeautifulSoup
startTime=time.clock()
def review_to_worldlist(review):
    review_text=BeautifulSoup(review,"html5lib").get_text()
    review_text=re.sub("[^a-zA-Z]","",review_text)
    #该正则用于匹配除了括号内以外的所有字符，即去除非字母。
    words=review_text.lower().split()
    return words
train=pd.read_csv("/Users/xutao/Downloads/Python/emoti-analysis/labeledTrainData.tsv",header=0,delimiter='\t',quoting=3)
test=pd.read_csv("/Users/xutao/Downloads/Python/emoti-analysis/testData.tsv",header=0,delimiter='\t',quoting=3)
#print train.head()
#print test.head()
y_train=train['sentiment']
train_data=[]
for i in xrange(0,len(train['review'])):
    print len(train['review'])
    train_data.append("-".join(review_to_worldlist(train['review'][i])))
    #.join()表示用空格来连接括号内的字符串
    print i

test_data=[]
for i in xrange(0,len(test['review'])):
    print i,len(test['review'])
    test_data.append("-".join(review_to_worldlist(test['review'][i])))
endTime=time.clock()
print train_data[0]
print "%d s"%(endTime-startTime)
from sklearn.feature_extraction.text import TfidfVectorizer as TFIV
tfv=TFIV(min_df=3,max_features=None,strip_accents='unicode',analyzer='word',token_pattern=r'\w{1,}',ngram_range=(1,2),use_idf=1,smooth_idf=1,sublinear_tf=1,stop_words='english')
X_all=train_data+test_data
len_train=len(train_data)

tfv.fit(X_all)
X_all=tfv.transform(X_all)
X=X_all[:len_train] #恢复训练集和测试集
X_test=X_all[len_train:]

from sklearn.naive_bayes import MultinomialNB as MNB
from sklearn.cross_validation import cross_val_score
model_NB=MNB()
model_NB.fit(X,y_train)
MNB(alpha=1.0,class_prior=None,fit_prior=True)
import numpy as np
print "MultinomialNB score:",cross_val_score(model_NB,X,y_train,cv=20,scoring='roc_auc')

#逻辑回归：
from sklearn.linear_model import LogisticRegression as LR
from sklearn.grid_search import GridSearchCV
grid_values={'C':[30]}
model_LR=GridSearchCV(LR(dual=True,random_state=0),grid_values,scoring='roc_auc',cv=20)
model_LR.fit(X,y_train)
GridSearchCV(cv=20, estimator=LR(C=1.0, class_weight=None, dual=True, 
        fit_intercept=True, intercept_scaling=1, penalty='L2', random_state=0, tol=0.0001),
        fit_params={}, iid=True, loss_func=None, n_jobs=1,
        param_grid={'C': [30]}, pre_dispatch='2*n_jobs', refit=True,
        score_func=None, scoring='roc_auc', verbose=0)
print model_LR.grid_scores_