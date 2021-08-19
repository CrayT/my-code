import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import classification_report
from pandas import Series,DataFrame
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
names = ['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']
data = pd.read_csv('/home/xutao/Downloads/Python/HEA-data/合并数据集-去除重复.csv',header=0,names=names)
Y = data[["class"]]

vars = ['1/(((logr)*(logrootHmix0-)))', '1/(((pow1/2RMS)*(logrootHmix0)))', '1/(((pow1/2VEC)*(pow3VEC)))', '1/(((pow3RMS)*(pow2rootHmix0)))', '1/(((logFi)*(pow3VEC)))', '1/(((pow3RMS)*(pow3rootHmix0)))', '1/(((pow2RMS)*(logVEC)))', '1/(((pow2VEC)*(pow1/2rootHmix0-)))']
X = pd.read_csv('/home/xutao/Downloads/Python/HEA-data/corelation.csv' )

#1/(((pow3RMS)*(pow2rootHmix0)))与1/(((pow3RMS)*(pow3rootHmix0)))相关性为1.
var = ['1/(((logr)*(logrootHmix0-)))', '1/(((pow1/2RMS)*(logrootHmix0)))', '1/(((pow1/2VEC)*(pow3VEC)))','1/(((pow3RMS)*(pow2rootHmix0)))', '1/(((logFi)*(pow3VEC)))', '1/(((pow2RMS)*(logVEC)))', '1/(((pow2VEC)*(pow1/2rootHmix0-)))']
x_tmp = X[var]

# x_tmp['class'] = np.array(Y['class'])
print(x_tmp.shape)
print(Y.shape)

# print(x_tmp.columns.values.tolist())

x_train,x_test,y_train,y_test = train_test_split(X,Y,test_size = 0.3, random_state = 33)

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

knc.fit(x_train,y_train)
dtc.fit(x_train,y_train)
rfc.fit(x_train,y_train)
gbc.fit(x_train,y_train)
abc.fit(x_train,y_train)
svc.fit(x_train,y_train)
gnb.fit(x_train,y_train)
LR.fit(x_train,y_train)

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

print("1:","KNC:",knc.score(x_test,y_test),'DTC:',dtc.score(x_test,y_test),"RFC:",rfc.score(x_test,y_test),\
"GBC:",gbc.score(x_test,y_test),"Ada:",abc.score(x_test,y_test),"SVC:",svc.score(x_test,y_test),\
"GauNB:",gnb.score(x_test,y_test),"LR:",LR.score(x_test,y_test))