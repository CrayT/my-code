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
#第一个图：
list_feature_num = np.arange(1,10) 
plt.subplot(1,2,1)
plt.ylim(0.5,1)
plt.yticks(np.linspace(0.5, 1, 6, endpoint = True)) 
plt.xticks(np.linspace(1, 9, 9, endpoint = True)) 
plt.scatter(list_feature_num, data1['train'], s = 55, marker = 'o', label = 'traning set')
plt.scatter(list_feature_num, data1['test'], s = 55, marker = ',', label = 'testing set')
plt.scatter(list_feature_num, list(data1['cross']), s = 75, marker = 'd', label = 'cross validation')
plt.plot(list_feature_num, data1['train'])
plt.plot(list_feature_num, data1['test'])
plt.plot(list_feature_num, data1['cross'])
plt.legend(loc = 'upper left')
# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)
plt.xlabel(u"descriptors num", font1)
plt.ylabel(u"accuracy", font1)
plt.grid(True, linestyle = "-.")

#第二个图：
plt.subplot(1,2,2)
list_feature_num2 = np.arange(1,21) 
plt.ylim(0.5,1)
plt.yticks(np.linspace(0.5, 1, 6, endpoint = True)) 
plt.xticks(np.linspace(2, 20, 10, endpoint = True)) 
plt.scatter(list_feature_num2, data2['train'], s = 55, marker = 'o', label = 'traning set')
plt.scatter(list_feature_num2, data2['test'], s = 55, marker = ',', label = 'testing set')
plt.scatter(list_feature_num2, data2['cross'], s = 75, marker = 'd', label = 'cross validation')
plt.plot(list_feature_num2, data2['train'])
plt.plot(list_feature_num2, data2['test'])
plt.plot(list_feature_num2, data2['cross'])
plt.legend(loc = 'upper left')
# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)
plt.xlabel(u"descriptors num", font1)
plt.ylabel(u"accuracy", font1)
plt.grid(True, linestyle = "-.")

plt.show()