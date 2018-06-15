#"UTF-8"
import matplotlib.pyplot as plt
#%matplotlib inline
import numpy as numpy
import pandas as pd
from sklearn import datasets,linear_model
data=pd.read_csv("/Users/xutao/Downloads/CCPP/1111.csv")
#print data.head()
#print data.shape
X=data[['AT','V','AP','RH']]
#print X.head()
Y=data[['PE']]
from sklearn.cross_validation import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,Y,random_state=0)
from sklearn.linear_model import LinearRegression
linreg=LinearRegression()
linreg.fit(X_train,y_train)
print linreg.intercept_
print linreg.coef_
y_predict=linreg.predict(X_test)
from sklearn import metrics
print "MSE:",metrics.mean_squared_error(y_predict,y_test)
from sklearn.model_selection import cross_val_predict
predicted=cross_val_predict(linreg,X,Y,cv=10)
print "MSE:",metrics.mean_squared_error(Y,predicted)
fig,ax=plt.subplots()
#ignore the parameter in blank(1,1) which means 1 column and 1 row,
# and back a figure(like a canvus) and a ax (like a subplot)
ax.scatter(Y,predicted)
ax.plot([Y.min(),Y.max()],[Y.min(),Y.max()],'k--',lw=4)
ax.set_ylabel("Predicted")
ax.set_xlabel("Measured")
plt.show()