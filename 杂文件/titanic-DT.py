#--coding:utf-8--
import pandas as pd
titanic=pd.read_csv("/home/xutao/Downloads/Python/data_set/titanic.txt")
feature_names=['pclass','age','sex']
target_names='survived'
x=titanic[feature_names]  #选取特征
y=titanic[target_names]
x['age'].fillna(30,inplace=True) #age缺失值使用平均值进行填充k

from sklearn.cross_validation import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=33)
#print(x_train)
from sklearn.feature_extraction import DictVectorizer
vec=DictVectorizer()
x_train=vec.fit_transform(x_train.to_dict(orient='record'))
x_test=vec.transform(x_test.to_dict(orient='record'))
#导入决策树模型
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
#print(x_train.shape)
#print(x_train[0])
#print(x_train)
dtc=DecisionTreeClassifier()
dtc.fit(x_train,y_train)
dtc_predict=dtc.predict(x_test)
import graphviz
tree.export_graphviz(dtc,out_file="tree.dot"  )

import pydotplus 
from IPython.display import Image
features=['A','B','C','D','E','F']
dot_data = tree.export_graphviz(dtc, out_file=None, 
feature_names=features, 
class_names=target_names, 
filled=True, rounded=True, special_characters=True) 
graph = pydotplus.graph_from_dot_data(dot_data) 
Image(graph.create_png())
graph.write_png('titanic-tree.png')

#导入随机森林模型
from sklearn.ensemble import RandomForestClassifier
tmp=0
for n in range(2,20):
    rfc=RandomForestClassifier(n_estimators=n,criterion='entropy',max_depth=10)
    rfc.fit(x_train,y_train)
    rfc_predict=rfc.predict(x_test)
    score=rfc.score(x_test,y_test)
    print "Accuracy of RFC,n_estimators=",n,":",score
    if tmp<score:
        tmp=score
print "max:",tmp
    
#导入梯度提升决策树模型
from sklearn.ensemble import GradientBoostingClassifier
gbc=GradientBoostingClassifier()
gbc.fit(x_train,y_train)
gbc_predict=gbc.predict(x_test)
from sklearn.metrics import classification_report
print "Accuracy of DT:",dtc.score(x_test,y_test)
print "Accuracy of RFC:",rfc.score(x_test,y_test)
print "Accuracy of GBC:",gbc.score(x_test,y_test)
#print classification_report(dtc_predict,y_test)
#print classification_report(rfc_predict,y_test)
#print classification_report(gbc_predict,y_test)