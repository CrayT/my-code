#coding:utf8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data1 = pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/小论文/数据/9个特征各项准确率-4-2.csv',header=0)
data2 = pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/小论文/数据/20个特征各项准确率4-5.csv',header=0)
print(data1.shape, data2.shape)
print(data1.columns.values.tolist())

font1 = {'family' : 'Times New Roman',
'weight' : 'bold',
'size'   : 20,
}
#设置输出的图片大小
figsize = 11,9
figure, ax = plt.subplots(figsize = figsize)
#设置坐标刻度值的大小以及刻度值的字体
plt.tick_params(labelsize = 18)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]


#可视化准确率与特征数量曲线图:
#第一个图：
list_feature_num = np.arange(1,10) 

list_feature_num2 = np.arange(1,21) 
plt.ylim(0.5,1)
plt.yticks(np.linspace(0.5, 1, 6, endpoint = True)) 
plt.xticks(np.linspace(2, 20, 10, endpoint = True)) 
#1B61A4 #1654C9
plt.scatter(list_feature_num2, data2['cross'], s = 75, edgecolors = '#1B61A4', marker = 's', linewidths = 3, c = '', label = 'selected descriptors')
plt.scatter(list_feature_num, data1['cross'], s = 60, edgecolors ='#F06D1E', c = '', linewidths = 3, marker = 'd', label = 'original descriptors')

font2 = {'family' : 'Times New Roman',
'weight' : 'normal',
'size'   : 20,
}
plt.legend(loc = 'upper left', prop = font2)

plt.axvline(9, ymin = 0,  ymax = 0.72, linestyle="--", linewidth = 1, color = '#1B61A4') #画垂直线
plt.axvline(6, ymin=0,  ymax = 0.5, linestyle="--", linewidth = 1, color='#F06D1E') #画垂直线

# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)

plt.xlabel(u"descriptors num", font1)
plt.ylabel(u"cross validation accuracy", font1)
plt.grid(True, linestyle = "-.")


plt.show()