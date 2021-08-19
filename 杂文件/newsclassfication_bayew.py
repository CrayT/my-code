import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
#Using KNN & Bayes for classification
#13 attributes:
Attribute_names=['class','Alcohol','Malic acid','Ash','Alcalinity of ash','Magnesium','Total phenols','Flavanoids','Nonflavanoid phenols','Proanthocyanins','Color intensity','Hue','diluted wines','Proline']
Data=pd.read_csv("/home/xutao/Downloads/Python/data_set/wine/wine.data.csv",names=Attribute_names)
#print Data.head()
#print Data['class'].shape
from sklearn.preprocessing import MinMaxScaler #[0,1]
mm=MinMaxScaler()
x_train,x_test,y_train,y_test=train_test_split(Data[Attribute_names[1:14]],Data[Attribute_names[0]],test_size=0.33,random_state=1)
#print x_train.head()
#print x_test
#print y_train
#print Data[Attribute_names[0:14]]
x_train=mm.fit_transform(x_train)  
x_test=mm.fit_transform(x_test)
#print x_train
from sklearn.naive_bayes import MultinomialNB
mnb=MultinomialNB()
mnb.fit(x_train,y_train)
y_predict_mnb=mnb.predict(x_test)
from sklearn.metrics import classification_report
print "Bayes accuracy:" ,mnb.score(x_test,y_test)
print classification_report(y_test,y_predict_mnb,target_names=None)

from sklearn.neighbors import KNeighborsClassifier #KNN
knn=KNeighborsClassifier()
knn.fit(x_train,y_train)
y_predict_knn=knn.predict(x_test)
print "KNN accuracy:",knn.score(x_test,y_test)
print classification_report(y_test,y_predict_knn,target_names=None)