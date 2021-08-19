import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFE
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_digits
from sklearn.cross_validation import cross_val_score
from sklearn.svm import SVC
from sklearn.model_selection import ShuffleSplit
from sklearn.preprocessing import StandardScaler,MaxAbsScaler
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

list_ranking=[113605, 113606, 113609, 113610, 113612, 113614, 113617, 113618, 113621, 113625, 113630, 113631, 113632, 113633, 113634, 113635, 113636, 113638, 113641, 113642, 113645, 113647, 113650, 113660, 113672, 113674, 113675, 113679, 113680, 113681, 113682, 113683, 113687, 113690, 113692, 113696, 113697, 113700, 113701, 113704, 113706, 113708, 113709, 113711, 113713, 113714, 113719, 113720, 113724, 113728, 113730, 113734, 113736, 113749, 113751, 113765, 113773, 113774, 113788, 113789, 113791, 113792, 113797, 113816, 113820, 113821, 113855, 113856, 113869, 113877, 113880, 113885, 113908, 113909, 113918, 113927, 114041, 114042, 114044, 114052, 114054, 114060, 114062, 114069, 114071, 114082, 114084, 114087, 114088, 114090, 114093, 114097, 114098, 114100, 114101, 114111, 114114, 114116, 114117, 114121]
list_ranking_importance=[58, 89, 53, 55, 94, 91, 82, 72, 74, 96, 25, 34, 41, 76, 17, 14, 5, 29, 81, 79, 24, 93, 98, 16, 77, 43, 97, 90, 19, 69, 20, 86, 26, 95, 61, 56, 39, 2, 49, 40, 44, 59, 60, 10, 23, 7, 50, 88, 70, 15, 37, 92, 46, 31, 78, 64, 4, 6, 51, 48, 66, 22, 62, 9, 33, 3, 18, 30, 67, 28, 35, 8, 42, 85, 13, 12, 63, 36, 75, 100, 84, 99, 21, 27, 1, 71, 65, 32, 11, 68, 54, 73, 52, 38, 83, 57, 87, 80, 45, 47]

list_ranking_inc=[] #从1开始的特征下标
list_ranking_importance_inc=[]#重要性从1开始到100的排序
for i in range(1,101):
    for j in range(0,100):
        if list_ranking_importance[j]==i:
            list_ranking_importance_inc.append(i)
            list_ranking_inc.append(list_ranking[list_ranking_importance.index(i)])
            break

list_feature_num=np.arange(1,101) 
list_feature_col=[]  ##存放特征数量,从1开始到100,分别存放特征的列标
for i in range(1,101):
    list_tmp=[]
    for num in list_feature_num:
        if int(num)<=int(i):
            list_tmp.append(num)
    list_feature_col.append(list(list_tmp))
    
list_feature_1=[] #分别存放重要性排序好之后的1个特征,2个特征...
for list_tmp in list_feature_col:
    tmp=[]
    for item in list_tmp:
        tmp.append(list_ranking_inc[item-1])
    list_feature_1.append(tmp)

names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']
data=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/合并数据集-去除重复.csv',header=0,names=names)
Y=data[["class"]]
X=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/generate_feature_1120.csv')

Y = np.array(Y).ravel()
list_accuracy_knc=[] #存放不同特征数量对应的准确率
list_accuracy_dtc=[]
list_accuracy_rfc=[]
list_accuracy_gbc=[]
list_accuracy_abc=[]
list_accuracy_svc=[]
list_accuracy_gnb=[]
list_accuracy_lr=[]
list_matrix=[]

list_tmp = list_feature_1[99]
print(list_tmp)
list_feature_1_1 = X.iloc[:,list_tmp].columns.values.tolist()


#替换最大值100000为该特征的最大值：
# for key in list_feature_1_1:
#         list_tmp = list(X[key])
#         flag = False
#         m = 0
#         for i in range(len(list_tmp)):
#             if int(X[key][i]) == 100000:
#                 flag = True
#                 m = X[key][i]
#                 break
#         if flag:
#             while m in list_tmp:
#                 list_tmp.remove(m)
#         max_value = max(list_tmp)
#         print("max:",max_value, m)
#         # print(x_tmp[key])
#         X[key]=X[key].replace(100000,max_value)

print(X)
#需要把训练集和测试集在for之前就分好，保持数据的一致性：
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3, random_state=33)

 #去均值和方差归一化,针对每一个特征维度，而不是针对样本


mas=MaxAbsScaler()
# x_train=mas.fit_transform(x_train)
# x_test=mas.transform(x_test)

iter = 1
for item in list_feature_1:
    print("Num: %s"%(iter))
    iter+=1
    knc=KNeighborsClassifier()
    dtc=DecisionTreeClassifier()
    rfc=RandomForestClassifier()
    gbc=GradientBoostingClassifier()
    abc=AdaBoostClassifier(n_estimators=10)
    svc=SVC(C=1, kernel='rbf', gamma='auto', coef0=0.0, shrinking=True, probability=False, tol=0.001, cache_size=200, class_weight=None, verbose=False)
    gnb = GaussianNB()
    LR=LogisticRegression()

    x_train_tmp = x_train.iloc[:,item]
    x_test_tmp = x_test.iloc[:,item]

    #归一化：
    ss = StandardScaler()
    x_train_tmp = ss.fit_transform(x_train_tmp)
    x_test_tmp = ss.transform(x_test_tmp)

    # mas = MaxAbsScaler()
    # x_train_tmp = mas.fit_transform(x_train_tmp)
    # x_test_tmp = mas.transform(x_test_tmp)

    knc.fit(x_train_tmp,y_train)
    dtc.fit(x_train_tmp,y_train)
    rfc.fit(x_train_tmp,y_train)
    gbc.fit(x_train_tmp,y_train)
    abc.fit(x_train_tmp,y_train)
    svc.fit(x_train_tmp,y_train)
    gnb.fit(x_train_tmp,y_train)
    LR.fit(x_train_tmp,y_train)

    list_accuracy_knc.append(knc.score(x_test_tmp,y_test))
    list_accuracy_dtc.append(dtc.score(x_test_tmp,y_test))
    list_accuracy_rfc.append(rfc.score(x_test_tmp,y_test))
    list_accuracy_gbc.append(gbc.score(x_test_tmp,y_test))
    list_accuracy_abc.append(abc.score(x_test_tmp,y_test))
    list_accuracy_svc.append(svc.score(x_test_tmp,y_test))
    list_accuracy_gnb.append(gnb.score(x_test_tmp,y_test))
    list_accuracy_lr.append(LR.score(x_test_tmp,y_test))

print("knc,dtc,rfc,gbc,abc,svc,gnb,lr")
for i in range(100):
    print(list_accuracy_knc[i],list_accuracy_dtc[i],list_accuracy_rfc[i],list_accuracy_gbc[i],\
    list_accuracy_abc[i],list_accuracy_svc[i],list_accuracy_gnb[i],list_accuracy_lr[i])
    # y_predict_rfc=rfc.predict(x_test_tmp)
    # list_matrix.append(confusion_matrix(y_test,y_predict_rfc))