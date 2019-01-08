#coding:utf8
#import featuretools as ft
import pandas as pd
import itertools
import math
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
from sklearn.feature_selection import RFE
print("finish")

names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']
data=pd.read_csv('合并数据集-去除重复.csv',header=0,names=names)
Y=data[["class"]]
X=pd.read_csv('generate_feature_1008.csv')
print("finish")

rfc=RandomForestClassifier()
#Y=Y.values
#Y= Y.reshape(c, )
rfe = RFE(estimator=rfc, n_features_to_select=1, step=1)
rfe.fit(X, Y)
ranking = rfe.ranking_
print("RFE ranking:\n",ranking)

list_ranking_index=[]
list_ranking_importance=[]
for i in range(len(ranking)):
    if ranking[i]<=100:
        list_ranking_index.append(i)
        list_ranking_importance.append(ranking[i])
print("list_ranking_index:\n",list_ranking_index)
print("list_ranking_importance:\n",list_ranking_importance)
print('finish')

#写入CSV
ranking_csv=pd.DataFrame(list_ranking_index,columns=['index'])
ranking_csv.insert(1,'importance',list_ranking_importance)
pd.DataFrame(ranking_csv).to_csv('/home/xutao/Downloads/Python/HEA-code/feature_index_importance.csv',index=False)

#可视化特征重要性
from sklearn.datasets import load_digits
digits = load_digits()
rank_rfe=list_ranking_importance.copy()
# Plot pixel ranking
ranking_plt = np.array(rank_rfe).reshape(10,10)

plt.matshow(ranking_plt, cmap=plt.cm.Blues)
plt.colorbar()
plt.title("Ranking of pixels with RFE")
plt.show()

'''
n_features=3:
    list_ranking:
        [113675, 113698, 114042]
rfc准确率:0.8455284552845529



n_features=20:
    list_ranking:
        [113635, 113636, 113675, 113697, 113700, 113708, 113710, 113711, 113733, 113736, 113751, 113769, 113775, 113855, 113856, 113877, 113894, 113895, 114034, 114090]    
rfc准确率:0.8780487804878049

'''

'''
#不经过降维: 
#1: KNC: 0.7723577235772358 DTC: 0.8455284552845529 RFC: 0.8536585365853658 
#   GBC: 0.8211382113821138 Ada: 0.6178861788617886 SVC: 0.6097560975609756 GauNB: 0.6097560975609756 LR: 0.2032520325203252

#经过PCA（20）降维:
#1: KNC: 0.8048780487804879 DTC: 0.6991869918699187 RFC: 0.7723577235772358 
#   GBC: 0.8211382113821138 Ada: 0.7886178861788617 SVC: 0.6097560975609756 GauNB: 0.6097560975609756 LR: 0.6097560975609756

#经过LDA(2)对训练集降维，对测试集进行转换:
#1: KNC: 0.6341463414634146 DTC: 0.5040650406504065 RFC: 0.5853658536585366 GBC: 0.6829268292682927 Ada: 0.6585365853658537 
#   SVC: 0.6097560975609756 GauNB: 0.6178861788617886 LR: 0.5203252032520326

#不降维直接进行分类：
#   RFC综合效果最好89.4%
#1: KNC: 0.7723577235772358 DTC: 0.8048780487804879 RFC: 0.8943089430894309 GBC: 0.8373983739837398 Ada: 0.6178861788617886 
#   SVC: 0.6097560975609756 GauNB: 0.6097560975609756 LR: 0.2032520325203252 LDA: 0.6341463414634146

'''