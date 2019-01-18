#--coding:utf-8--
#对良/恶性肿瘤分类
import pandas as pd
import numpy as np
column_names=['Sample code number','Clump thickness','Cell size','cell shape','marginal adhesion','single cell size','bare nuclei','Bland chromatin','normal nucleoli','mitoses','class']
data=pd.read_csv('/home/xutao/Downloads/Python/data_set/breast-cancer/breast-cancer.csv',names=column_names)
#print data.shape
data=data.replace(to_replace="?",value=np.nan)
#数据集中有？，将其换为标准缺失值
data=data.dropna(how='any') #只要有一个维度数据有却失，就将数据丢掉
from sklearn.cross_validation import train_test_split
x_train,x_test,y_train,y_test=train_test_split(data[column_names[1:10]],data[column_names[10]],test_size=0.25,random_state=33)
#random_state为随机数种子，若为0，则每次产生的随机数都一样。
print y_train.shape #524条
print x_train.shape #524条
print x_test.shape #175条
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier  #随机梯度下降法
#标准化数据，使得每个维度的数据方差为1，均值为0，以防出现过大数据
ss=StandardScaler()
x_train=ss.fit_transform(x_train)
x_test=ss.fit_transform(x_test)
LR=LogisticRegression()
SGDC=SGDClassifier()
LR.fit(x_train,y_train)
LR_predicted=LR.predict(x_test)
SGDC.fit(x_train,y_train)
#SGDC_predicted=SGDC.predict(x_test)
from sklearn.metrics import classification_report
print "LR:",LR.score(x_test,y_test)
print "SGDC:",SGDC.score(x_teStandardScalerst,y_test)
print LR.coef_
#LR的其他三个指标
print classification_report(y_test,LR_predicted,target_names=['Benign','worse'])