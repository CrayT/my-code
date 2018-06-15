#--coding:utf-8-
from sklearn.datasets import load_boston
boston=load_boston()
#print boston
from sklearn.cross_validation import train_test_split
import numpy as np
x=boston.data
y=boston.target
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25,random_state=33)
from sklearn.svm import SVR
linear_svr=SVR(kernel='linear')#线性核函数
linear_svr.fit(x_train,y_train)
ls_predict=linear_svr.predict(x_test)
print linear_svr.score(x_test,y_test)

#poly_svr=SVR(kernel='poly')#多项式核函数
#poly_svr.fit(x_train,y_train)
#ps_predict=poly_svr.predict(x_test)
#print poly_svr.score(x_test,y_test)

r_svr=SVR(kernel='rbf')#径向基核函数
r_svr.fit(x_train,y_train)
r_predict=r_svr.predict(x_test)
print r_svr.score(x_test,y_test)

from sklearn.neighbors import KNeighborsRegressor
#k近邻回归，对最近的k个类别数值采用平均值，还有一种加权方式，weights=distance
knr=KNeighborsRegressor(weights='uniform') 
knr.fit(x_train,y_train)
knr_predict=knr.predict(x_test)
print knr.score(x_test,y_test)