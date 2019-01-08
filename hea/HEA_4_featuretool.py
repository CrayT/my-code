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
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_selection import RFE
from feature_create import *
from sklearn.linear_model import Lasso
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import r2_score

names=['alloy','num','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']

data=pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/HEA/feature_tools/合并数据集-去除重复.csv',header=0,names=names)
#X=data[['delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']]
Y=data[["class"]]


#X_new=create_features(X,X)

#X_gen_fea=generate_feature(X)
#X_gen_fea.to_csv('/Users/xutao/Downloads/Python/HEA/HEA-code/generate_feature.csv',index=False)

data_generate=pd.read_csv('/Users/xutao/Downloads/Python/HEA/HEA-code/generate_feature.csv')
X_new=data_generate
print(X_new.shape)


#将含有NaN的列(columns)去掉:
#X =X.dropna(axis=1)
#print(X_new.shape)

lda = LinearDiscriminantAnalysis(n_components=2)   
lda.fit(X_new,Y)
X_new = lda.transform(X_new)  #能否找出LDA降维后的特征与原始数据之间的映射关系。
print(X_new)
# pca=PCA(n_components=15)
# pca.fit(X_new)
# X_new=pca.transform(X_new) #PCA进行降维

# 基于l1正则化的特征选择
# model = SelectFromModel(lsvc, prefit=True)




x_train,x_test,y_train,y_test=train_test_split(X_new,Y,test_size=0.3, random_state=1)

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


from sklearn.metrics import classification_report

print('\n1:')
print("DTC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_dtc))
print("\nKNC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_knc))
print("\nRFC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_rfc))
print("\nGBC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_gbc))
print("\nAda confusioin_matrix:\n",confusion_matrix(y_test,y_predict_abc))
print("\nSVC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_svc))
print("\nLR confusioin_matrix:\n",confusion_matrix(y_test,y_predict_lr))

print("1:","KNC:",knc.score(x_test,y_test),'DTC:',dtc.score(x_test,y_test),"RFC:",rfc.score(x_test,y_test),"GBC:",gbc.score(x_test,y_test),\
"Ada:",abc.score(x_test,y_test),"SVC:",svc.score(x_test,y_test),"GauNB:",gnb.score(x_test,y_test),\
"LR:",LR.score(x_test,y_test))



c, r = Y.shape 
Y=Y.values
Y= Y.reshape(c, )
rfe = RFE(estimator=rfc, n_features_to_select=2, step=1)
rfe.fit(X_new, Y)
ranking = rfe.ranking_
print("RFE ranking:\n",ranking)

