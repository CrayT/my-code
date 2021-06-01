#coding:utf8
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

list_feature_num=np.arange(1,29) 

data1 = pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/小论文/数据/9+20个特征准确率-3-21.csv',header=0)
data2 = pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/小论文/数据/训练集准确率3-27.csv', header = 0)
print(data1.shape, data2.shape)

font1 = {'family' : 'Times New Roman',
'weight' : 'bold',
'size'   : 18,
}
#设置输出的图片大小
figsize = 11,9
figure, ax = plt.subplots(figsize = figsize)
#设置坐标刻度值的大小以及刻度值的字体
plt.tick_params(labelsize = 12)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]

#可视化准确率与特征数量曲线图:
plt.ylim(0.4,1)
plt.yticks(np.linspace(0.4, 1, 7, endpoint = True)) 
plt.xticks(np.linspace(1, 29, 15, endpoint = True)) 
plt.scatter(list_feature_num, data1, s = 55, marker = '*', label = 'test set')
plt.scatter(list_feature_num, data2, s = 45, marker = 'D', label = 'traning set')
plt.legend(loc = 'upper left')

# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)

# plt.text(50,-0.1,"descriptors num",font1)

plt.xlabel(u"descriptors num", font1)
plt.ylabel(u"accuracy", font1)
plt.grid(True, linestyle = "-.")
plt.show()