#--coding:utf-8--
import pandas as pd
import numpy as np
train=pd.read_csv("/Users/xutao/Downloads/Python/Sanf/train.csv")
test=pd.read_csv("/Users/xutao/Downloads/Python/Sanf/test.csv")
#print train[:5]
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing
leCrime=preprocessing.LabelEncoder()
crime=leCrime.fit_transform(train.Category)#将crime类型进行encode，即不同类型用不同的数字编号。
#print crime[:10]
days=pd.get_dummies(train.DayOfWeek)
district=pd.get_dummies(train.PdDistrict)
#pd.to_datetime(train.Dates)
#hour=train.Dates.dt.hour
#hour=pd.get_dummies(hour)
#print hour[:10]
trainData=pd.concat([days,district],axis=1)
#axis=1为行拼接，为0位列拼接
trainData['crime']=crime
days=pd.get_dummies(test.DayOfWeek)
#用get_dummies将DayOfWeek二值化，即分化为7个星期几的类别，在星期几，对应类目下就为1.否则为0
district=pd.get_dummies(test.PdDistrict)
#hour=test.Dates.dt.hour
#hour=pd.get_dummies(hour)
testData=pd.concat([days,district],axis=1) #用concat将二值化后的向量行拼接。接下来的训练就用这些属性进行训练。
#print trainData.head()
from sklearn.metrics import log_loss
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
import time
features=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','BAYVIEW','CENTRAL','INGLESIDE','MISSION','NORTHERN','PARK','RICHMOND','SOUTHERN','TARAVAL','TENDERLOIN']
training,validation=train_test_split(trainData,train_size=.80)
model=BernoulliNB()
nbStart=time.time()
model.fit(training[features],training['crime'])
nbCostTime=time.time()-nbStart
predicted=np.array(model.predict_proba(validation[features]))
print "NB time:%fs"%(nbCostTime)
print "NB loss: %f"%(log_loss(validation['crime'],predicted))

model=LogisticRegression(C=.01)
#C值默认为1，约束条件，C值越小，正则化强度越大。
print "Logistic Traing..."
lrStart=time.time()
model.fit(training[features],training['crime'])
lrCostTime=time.time()-lrStart
predicted=np.array(model.predict_proba(validation[features]))
#predict_proba返回每个样本的每个类别的预测概率
print "Logistic time: %fs"%(lrCostTime)
print "Logistic loss: %f"%(log_loss(validation['crime'],predicted))
