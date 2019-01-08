#!/usr/bin/env python
#coding:utf8
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.model_selection import learning_curve
from sklearn.feature_selection import RFE
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import warnings
from sklearn.svm import SVC
from sklearn.model_selection import ShuffleSplit
from sklearn.preprocessing import StandardScaler,MaxAbsScaler
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

from sklearn.feature_selection import RFE

from feature_create import create_features,generate_feature,generate_feature_step2


names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']

data=pd.read_csv('/home/xutao/Downloads/Python/HEA-code/合并数据集-去除重复.csv',header=0,names=names)
X=data[['delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']]
Y=data[["class"]]

#X=create_features(X,X)

X_gen_fea=generate_feature(X)
X_gen_fea.to_csv('/home/xutao/Downloads/Python/HEA-code/generate_feature_1008_tmp.csv',index=False)

data_tmp=pd.read_csv('/home/xutao/Downloads/Python/HEA-code/generate_feature_1008_tmp.csv',header=0)
X_gen_fea=generate_feature_step2(data_tmp)
X_gen_fea.to_csv('/home/xutao/Downloads/Python/HEA-code/generate_feature_1008.csv',index=False)


X=pd.read_csv('/home/xutao/Downloads/Python/HEA-code/generate_feature_1008.csv')
#X=X_gen_fea
print(X.shape)

#将含有NaN的列(columns)去掉:
#X =X.dropna(axis=1)
#print(X_new.shape)
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(n_components=2)

# lda.fit(X,Y)
# X = lda.transform(X)

# print(X.shape)
# coef=lda.coef_
# #print("权重向量：",coef,'\n',"权重向量长度：",len(lda.coef_))
# print("权重向量shape:",coef.shape)
# #print("迭代次数:",lda.n_iter_)
# print("intercept:",lda.intercept_)
# print("截距长度：",len(lda.intercept_))

#print(X_new)
# pca=PCA(n_components=2)
# pca.fit(X)
# X=pca.transform(X) #PCA进行降维

#矩阵相乘:
#np.dot(b,a)


x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3, random_state=33)


print("\ny_test:")
print(y_test['class'].value_counts())

print("\ny_train:")
print(y_train['class'].value_counts())

mnb=MultinomialNB()
knc=KNeighborsClassifier()
dtc=DecisionTreeClassifier()
rfc=RandomForestClassifier()
gbc=GradientBoostingClassifier()
abc=AdaBoostClassifier(n_estimators=10)
svc=SVC(C=1, kernel='rbf', gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False)
gnb = GaussianNB()
LR=LogisticRegression()

#reshape  y_train的形状:
c, r = y_train.shape 
y_train=y_train.values
y_train= y_train.reshape(c, )



#mnb.fit(x_train,y_train)
knc.fit(x_train,y_train)
dtc.fit(x_train,y_train)
rfc.fit(x_train,y_train)
gbc.fit(x_train,y_train)
abc.fit(x_train,y_train)
svc.fit(x_train,y_train)
gnb.fit(x_train,y_train)
LR.fit(x_train,y_train)

#y_predict_mnb=mnb.predict(x_test)
y_predict_knc=knc.predict(x_test)
y_predict_dtc=dtc.predict(x_test)
y_predict_rfc=rfc.predict(x_test)
y_predict_gbc=gbc.predict(x_test)
y_predict_abc=abc.predict(x_test)
y_predict_svc=svc.predict(x_test)
y_predict_gnb=gnb.predict(x_test)
y_predict_lr=LR.predict(x_test)
print("finish")


# In[23]:


from sklearn.metrics import classification_report

print('\n1:')
print("DTC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_dtc))
print("\nKNC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_knc))
print("\nRFC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_rfc))
print("\nGBC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_gbc))
print("\nAda confusioin_matrix:\n",confusion_matrix(y_test,y_predict_abc))
print("\nSVC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_svc))
print("\nLR confusioin_matrix:\n",confusion_matrix(y_test,y_predict_lr))

print("1:","KNC:",knc.score(x_test,y_test),'DTC:',dtc.score(x_test,y_test),"RFC:",rfc.score(x_test,y_test),"GBC:",gbc.score(x_test,y_test),"Ada:",abc.score(x_test,y_test),"SVC:",svc.score(x_test,y_test),"GauNB:",gnb.score(x_test,y_test),"LR:",LR.score(x_test,y_test))



# In[ ]:




import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Y=pd.DataFrame(Y)
# plt.scatter(X[:, 0], X[:, 1],marker='o',c=np.squeeze(Y))
# # plt.title("PCA")
# plt.show()