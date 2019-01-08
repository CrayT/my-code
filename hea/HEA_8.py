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


list_feature_num=np.arange(1,101) 


names=['num','knc','dtc','rfc','gbc','abc','svc','gnb','lr']
data=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/准确率.csv',header=0,names=names)


list_accuracy_knc=data['knc'] #存放不同特征数量对应的准确率
list_accuracy_dtc=data['dtc']
list_accuracy_rfc=data['rfc']
list_accuracy_gbc=data['gbc']
list_accuracy_abc=data['abc']
list_accuracy_svc=data['svc']
list_accuracy_gnb=data['gnb']
list_accuracy_lr=data['lr']


font1 = {'family' : 'Times New Roman',
'weight' : 'bold',
'size'   : 12,
}
#设置输出的图片大小
figsize = 11,9
figure, ax = plt.subplots(figsize=figsize)
#设置坐标刻度值的大小以及刻度值的字体
plt.tick_params(labelsize=12)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]

#可视化准确率与特征数量曲线图:
plt.ylim(0,1)
plt.yticks(np.linspace(0,1,11,endpoint=True)) 
plt.scatter(list_feature_num,list_accuracy_rfc,s=5,marker='o')

order=4 #阶数
c=np.polyfit(list_feature_num,list_accuracy_rfc,deg=order)
x_new=np.linspace(0,100,200)
f_liner=np.polyval(c,x_new)
plt.plot(x_new,f_liner,label='拟合曲线',color='g',linewidth=3,linestyle='-',marker='')

plt.axvline(8, linestyle="-", linewidth=2, color='g') #画垂直线

plt.xlabel(u"descriptors num",font1)
plt.ylabel(u"accuracy",font1)
plt.grid(True, linestyle = "-.")
plt.show()