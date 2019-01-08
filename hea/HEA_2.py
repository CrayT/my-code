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


def versiontuple(v):#Numpy版本检测函数
    return tuple(map(int, (v.split("."))))  


def plot_decision_regions(X, y, classifier, test_idx=None, resolution=0.02):
    #画决策边界,X是特征，y是标签，classifier是分类器，test_idx是测试集序号
    # setup marker generator and color map
    markers = ('s', 'x', 'o', '^', 'v')
    colors = ('red', 'blue', 'lightgreen', 'gray', 'cyan')
    cmap = ListedColormap(colors[:len(np.unique(y))])

    # plot the decision surface
    x1_min, x1_max = X[:, 0].min() - 1, X[:, 0].max() + 1   #第一个特征取值范围作为横轴
    x2_min, x2_max = X[:, 1].min() - 1, X[:, 1].max() + 1   #第二个特征取值范围作为纵轴
    xx1, xx2 = np.meshgrid(np.arange(x1_min, x1_max, resolution),
                           np.arange(x2_min, x2_max, resolution))  #reolution是网格剖分粒度，xx1和xx2数组维度一样
    Z = classifier.predict(np.array([xx1.ravel(), xx2.ravel()]).T)   
    #classifier指定分类器，ravel是数组展平；Z的作用是对组合的二种特征进行预测
    Z = Z.reshape(xx1.shape)   #Z是列向量
    plt.contourf(xx1, xx2, Z, alpha=0.4, cmap=cmap)  
    #contourf(x,y,z)其中x和y为两个等长一维数组，z为二维数组，指定每一对xy所对应的z值。
    #对等高线间的区域进行填充（使用不同的颜色）
    plt.xlim(xx1.min(), xx1.max())
    plt.ylim(xx2.min(), xx2.max())

    for idx, cl in enumerate(np.unique(y)):
        plt.scatter(x=X[y == cl, 0], y=X[y == cl, 1],
                    alpha=0.8, c=cmap(idx),
                    marker=markers[idx], label=cl)   #全数据集，不同类别样本点的特征作为坐标(x,y)，用不同颜色画散点图

    # highlight test samples
    if test_idx:
        # plot all samples
        if not versiontuple(np.__version__) >= versiontuple('1.9.0'):
            X_test, y_test = X[list(test_idx), :], y[list(test_idx)]
            warnings.warn('Please update to NumPy 1.9.0 or newer')
        else:
            X_test, y_test = X[test_idx, :], y[test_idx]   #X_test取测试集样本两列特征，y_test取测试集标签

        plt.scatter(X_test[:, 0],
                    X_test[:, 1],
                    c='',
                    alpha=1.0,
                    linewidths=1,
                    marker='o',
                    s=55, label='test set')   #c设置颜色，测试集不同类别的实例点画图不区别颜色

estimator=PCA(n_components=5)

#所有共有属性集合:
#SVC=93.63:['delta','Smix','RMS', 'VEC','r', 'Sc', 'deltaHmixmin', 'rootHmix', 'rootHmix0+']
#SVC :93.13 ['delta','Smix', 'VEC', 'Sc']
x_parameter_collection=['delta','Smix', 'VEC', 'Sc']

names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']
data=pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/HEA/合并数据集-去除重复.csv',header=0,names=names) #/Users/xutao/Nustore Files/我的坚果云/HEA #/Users/xutao/Downloads/Python/HEA/

Y=data[["class"]]
X=data[x_parameter_collection]
Alloy=data[['alloy']]

print(X.shape)

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25, random_state=1)

#print(type(x_test))

print("\ny_test:")
print(y_test['class'].value_counts())

print("\ny_train:")
print(y_train['class'].value_counts())




ss=StandardScaler() #去均值和方差归一化,针对每一个特征维度，而不是针对样本
# x_train=ss.fit_transform(x_train)
# x_test=ss.transform(x_test)

mas=MaxAbsScaler()
# x_train=mas.fit_transform(x_train)
# x_test=mas.transform(x_test)

#print(x_train)

#print("X_test:",X_test)

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

'''
print "KNC:",classification_report(y_test,y_predict_knc)
print "DTC:",classification_report(y_test,y_predict_dtc)
print "RFC:",classification_report(y_test,y_predict_rfc)
print "GBC:",classification_report(y_test,y_predict_gbc)
print "ADa:",classification_report(y_test,y_predict_abc)
print "SVC:",classification_report(y_test,y_predict_svc)
'''


#GBC的预测最高,下面输出预测结果：
# print("\nGBC prediction:")
# for i in range(len(y_test)):
#     print('{0:<50}\t{1:^2}\t{2:^2}'.format(str(Y_test_alloy['alloy'][i]),str(y_test['class'][i]),str(y_predict_abc[i])))

print('\n1:')
print "DTC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_dtc)
print "\nKNC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_knc)
print "\nRFC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_rfc)
print "\nGBC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_gbc)
print "\nAda confusioin_matrix:\n",confusion_matrix(y_test,y_predict_abc)
print "\nSVC confusioin_matrix:\n",confusion_matrix(y_test,y_predict_svc)
print "\nLR confusioin_matrix:\n",confusion_matrix(y_test,y_predict_lr)


#print(y_train.shape,y_test.shape,x_train.shape,x_test.shape)

def plot_learning_curve(estimator, title, X, y, ylim=None, cv=None,
                        n_jobs=1, train_sizes=np.linspace(.1, 1.0, 5)):
    """
    Generate a simple plot of the test and training learning curve.

    Parameters
    ----------
    estimator : object type that implements the "fit" and "predict" methods
        An object of that type which is cloned for each validation.

    title : string
        Title for the chart.

    X : array-like, shape (n_samples, n_features)
        Training vector, where n_samples is the number of samples and
        n_features is the number of features.

    y : array-like, shape (n_samples) or (n_samples, n_features), optional
        Target relative to X for classification or regression;
        None for unsupervised learning.

    ylim : tuple, shape (ymin, ymax), optional
        Defines minimum and maximum yvalues plotted.

    cv : int, cross-validation generator or an iterable, optional
        Determines the cross-validation splitting strategy.
        Possible inputs for cv are:
          - None, to use the default 3-fold cross-validation,
          - integer, to specify the number of folds.
          - An object to be used as a cross-validation generator.
          - An iterable yielding train/test splits.

        For integer/None inputs, if ``y`` is binary or multiclass,
        :class:`StratifiedKFold` used. If the estimator is not a classifier
        or if ``y`` is neither binary nor multiclass, :class:`KFold` is used.

        Refer :ref:`User Guide <cross_validation>` for the various
        cross-validators that can be used here.

    n_jobs : integer, optional
        Number of jobs to run in parallel (default 1).
    """
    plt.figure()
    plt.title(title)
    if ylim is not None:
        plt.ylim(*ylim)
    plt.xlabel("Training examples")
    plt.ylabel("Score")
    train_sizes, train_scores, test_scores = learning_curve(
        estimator, X, y, cv=cv, n_jobs=n_jobs, train_sizes=train_sizes)
    train_scores_mean = np.mean(train_scores, axis=1)
    train_scores_std = np.std(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    test_scores_std = np.std(test_scores, axis=1)
    plt.grid()

    plt.fill_between(train_sizes, train_scores_mean - train_scores_std,
                     train_scores_mean + train_scores_std, alpha=0.1,
                     color="r")
    plt.fill_between(train_sizes, test_scores_mean - test_scores_std,
                     test_scores_mean + test_scores_std, alpha=0.1, color="g")
    plt.plot(train_sizes, train_scores_mean, 'o-', color="r",
             label="Training score")
    plt.plot(train_sizes, test_scores_mean, 'o-', color="g",
             label="Cross-validation score")

    plt.legend(loc="best")
    return plt


# digits = load_digits()
# X, y = digits.data, digits.target

'''
title = "Learning Curves (Naive Bayes)"
# Cross validation with 100 iterations to get smoother mean test and train
# score curves, each time with 20% data randomly selected as a validation set.
cv = ShuffleSplit(n_splits=100, test_size=0.2, random_state=0)

estimator = KNeighborsClassifier()
plot_learning_curve(estimator, title, X, Y, ylim=(0.7, 1.01), cv=cv, n_jobs=4)

title = "Learning Curves (SVM, RBF kernel, $\gamma=0.001$)"
# SVC is more expensive so we do a lower number of CV iterations:
cv = ShuffleSplit(n_splits=10, test_size=0.25, random_state=0)
estimator = SVC(gamma=0.001)
plot_learning_curve(estimator, title, X, Y, (0.7, 1.01), cv=cv, n_jobs=4)

plt.show()
'''

c, r = Y.shape 
Y=Y.values
Y = Y.reshape(c, )

#交叉验证:
scores = cross_val_score(svc, X, Y, cv=10)#, scoring='accuracy')
print("\n交叉验证 SVC:\n"+ str(scores))

print("\n特征重要性评级:")
print("RFC feature importance:\n"+str(rfc.feature_importances_) )
print("\nGBC feature importance:\n"+str(gbc.feature_importances_) )

'''
#画出分类面,训练集需要是两个维度：
c, r = y_test.shape 
y_test=y_test.values
y_test = y_test.reshape(c, )
X_combined_std = np.vstack((x_train, x_test))   #shape是(150,2)  

y_combined = np.hstack((y_train, y_test))   #shape是(150,)  
  
plot_decision_regions(X=X_combined_std, y=y_combined,  
                      classifier=svc, test_idx=range(105, 150))  
plt.xlabel('parameter1')  
plt.ylabel('parameter2')  
plt.legend(loc='upper left')  
  
plt.tight_layout()   #紧凑显示图片，居中显示；避免出现叠影  
# plt.savefig('./figures/iris_perceptron_scikit.png', dpi=300)  
plt.show()  
'''

print "1:","KNC:",knc.score(x_test,y_test),'DTC:',dtc.score(x_test,y_test),"RFC:",rfc.score(x_test,y_test),"GBC:",gbc.score(x_test,y_test),\
"Ada:",abc.score(x_test,y_test),"SVC:",svc.score(x_test,y_test),"GauNB:",gnb.score(x_test,y_test),\
"LR:",LR.score(x_test,y_test)
