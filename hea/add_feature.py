#coding:utf8
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
import itertools
import pandas as pd
from pandas import Series,DataFrame
import numpy as np
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
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
from sklearn.ensemble import ExtraTreesClassifier

names=['alloy','num','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']
data=pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/HEA/feature_tools/合并数据集-去除重复.csv',header=0,names=names)
X=data[['delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']]
Y=data[["class"]]
features=['delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']

features_2=[] #得到所有两个特征的组合数组：
for item in itertools.combinations(features,2):
    features_2.append(item)

print(X.shape)
#print(len(features_2))
c,r=X.shape
operator=['*','/']
dim=r
for m in range(len(features_2)):
    a=X[features_2[m][0]]
    b=X[features_2[m][1]]
    for k in range(len(operator)):
        c=[]
        op=operator[k]
        for i in range(len(a)):
            if op=='+':
                c.append(a[i]+b[i])
            elif op=='-':
                c.append(a[i]-b[i])
            elif op=='*':
                c.append(a[i]*b[i])
            elif op=='/':
                if b[i]==0:
                    c.append(1000000)
                else:
                    c.append(a[i]/b[i])
        name=features_2[m][0]+str(op)+features_2[m][1]
        X.insert(dim,"%s"%name,c)
        dim=dim+1
print("第一次升维:",X.shape)

column_index=X.columns

for i in range(len(column_index)):
    c=[]
    a=X[column_index[i]]
    for j in range(len(a)):
        if a[j]!=0:
            c.append(1/a[j])
        else:
            c.append(100000)
    name='1/'+column_index[i]
    X.insert(dim,'%s'%name,c)
    dim=dim+1
print("第二次升维:",X.shape)


lda = LinearDiscriminantAnalysis(n_components=4)
lda.fit(X,Y)
X = lda.transform(X)


# clf = ExtraTreesClassifier()
# X_new = clf.fit(X, Y)

#print(clf.feature_importances_ ) 

# from sklearn.feature_selection import SelectKBest,chi2 #X中特征取值必须非负
# X_new=SelectKBest(chi2,k=2).fit_transform(X,Y)

# pca=PCA(n_components=10)
# pca.fit(X)
# X=pca.transform(X) #PCA进行降维

print("LDA降维后:",X.shape)
# print(X)
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3, random_state=1)


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
print("\nGauNB confusioin_matrix:\n",confusion_matrix(y_test,y_predict_gnb))
print("\nLR confusioin_matrix:\n",confusion_matrix(y_test,y_predict_lr))

print("1:","KNC:",knc.score(x_test,y_test),'DTC:',dtc.score(x_test,y_test),"RFC:",rfc.score(x_test,y_test),"GBC:",gbc.score(x_test,y_test),\
"Ada:",abc.score(x_test,y_test),"SVC:",svc.score(x_test,y_test),"GauNB:",gnb.score(x_test,y_test),\
"LR:",LR.score(x_test,y_test))



c, r = Y.shape
Y=Y.values
Y= Y.reshape(c, )

dtc1=DecisionTreeClassifier()
gbc1=GradientBoostingClassifier()
gnb1 = GaussianNB()

rfe = RFE(estimator=gnb1, n_features_to_select=5, step=1)
rfe.fit(X, Y)
ranking = rfe.ranking_
print("gnb RFE ranking:\n",ranking)

#print(X.index)
#print(X.iloc[0])