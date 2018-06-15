Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 12:39:47) 
[GCC 4.2.1 (Apple Inc. build 5666) (dot 3)] on darwin
Type "copyright", "credits" or "license()" for more information.
>>> WARNING: The version of Tcl/Tk (8.5.9) in use may be unstable.
Visit http://www.python.org/download/mac/tcltk/ for current information.

>>> 
>>> #使用支持向量机分类器处理Scikit-learn内部集成的手写体数字图片数据集

>>> from sklearn.datasets import load_digits
>>> digits=load_digits()
>>> digits.data.shape
(1797, 64)
>>> from sklearn.cross_validation import train_test_split

Warning (from warnings module):
  File "/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/sklearn/cross_validation.py", line 44
    "This module will be removed in 0.20.", DeprecationWarning)
DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note that the interface of the new CV iterators are different from that of this module. This module will be removed in 0.20.
>>> x_train,x_test,y_train,y_test=train_test_split(digits.data,digits.target,test_size=0.25,random_state=33)
>>> y_train.shape
(1347,)
>>> y_test.shape
(450,)
>>> from sklearn.preprocessing import StandardScaler
>>> from sklearn.svm import LinearSVC
>>> ss=StandardScaler()
>>> x_train=ss.fit_transform(x_train)
>>> x_test=ss.transform(x_test)
>>> lsvc=LinearSVC()
>>> lsvc.fit(x_train,y_train)
LinearSVC(C=1.0, class_weight=None, dual=True, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
     verbose=0)
>>> y_predict=lsvc.predict(x_test)
>>> print "the Accuracy of LinearSVC is",lsvc.score(x_test,y_test)
the Accuracy of LinearSVC is 0.953333333333
>>> from sklearn,metrics import classification_report
SyntaxError: invalid syntax
>>> from sklearn.metrics import classification_report
>>> print classification_report(y_test,y_predict,target_names=digits.target_names.astype(str))
             precision    recall  f1-score   support

          0       0.92      1.00      0.96        35
          1       0.96      0.98      0.97        54
          2       0.98      1.00      0.99        44
          3       0.93      0.93      0.93        46
          4       0.97      1.00      0.99        35
          5       0.94      0.94      0.94        48
          6       0.96      0.98      0.97        51
          7       0.92      1.00      0.96        35
          8       0.98      0.84      0.91        58
          9       0.95      0.91      0.93        44

avg / total       0.95      0.95      0.95       450

>>> 
