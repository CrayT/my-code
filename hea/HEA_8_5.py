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
plt.subplot(1, 2, 1)
plt.ylim(0.5, 0.9)
plt.yticks(np.linspace(0.5, 0.9, 5, endpoint = True)) 
plt.xticks(np.linspace(1, 9, 9, endpoint = True)) 
# plt.scatter(list_feature_num, data1['train'], s = 55, edgecolors = 'b', c = '', linewidths = 2,marker = 'o', label = 'traning set')
# plt.scatter(list_feature_num, data1['test'], s = 55, edgecolors ='orange', c = '',linewidths = 2, marker = ',', label = 'testing set')
plt.scatter(list_feature_num, data1['cross'], s = 75, edgecolors ='g', c = '', linewidths = 2, marker = '*', label = 'cross validation')
# plt.legend(loc = 'upper left')

order = 5 #阶数
# c1 = np.polyfit(list_feature_num, data1['train'], deg = 3)
# c2 = np.polyfit(list_feature_num, data1['test'], deg = 3)
c3 = np.polyfit(list_feature_num, data1['cross'], deg = order)
x_new = np.linspace(1, 9, 27)
# f_liner1 = np.polyval(c1, x_new)
# f_liner2 = np.polyval(c2, x_new)
f_liner3 = np.polyval(c3, x_new)
# plt.plot(x_new, f_liner1, label = '拟合曲线', color='b',linewidth = 2,linestyle='-', marker='')
# plt.plot(x_new, f_liner2, label = '拟合曲线', color='orange',linewidth = 2,linestyle='-', marker='')
# plt.plot(x_new, f_liner3, label = '拟合曲线', color='r',linewidth = 2,linestyle='-', marker='')
plt.axvline(6, ymin=0,  ymax = 0.625, linestyle="--", linewidth = 1, color='b') #画垂直线
# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)
plt.xlabel(u"descriptors num", font1)
plt.ylabel(u"cross validation accuracy", font1)
plt.grid(True, linestyle = "-.")

#第二个图：
plt.subplot(1,2,2)
list_feature_num2 = np.arange(1,21) 
plt.ylim(0.5,1)
plt.yticks(np.linspace(0.5, 1, 6, endpoint = True)) 
plt.xticks(np.linspace(2, 20, 10, endpoint = True)) 
# plt.scatter(list_feature_num2, data2['train'], s = 55, edgecolors = 'b', marker = 'o', linewidths = 2, c = '', label = 'traning set')
# plt.scatter(list_feature_num2, data2['test'], s = 55, edgecolors = 'orange', marker = ',', linewidths = 2, c = '', label = 'testing set')
plt.scatter(list_feature_num2, data2['cross'], s = 75, edgecolors = 'g', marker = '*', linewidths = 2, c = '', label = 'cross validation')
# plt.legend(loc = 'upper left')

order = 8 #阶数
# c1 = np.polyfit(list_feature_num2,data2['train'], deg = order)
# c2 = np.polyfit(list_feature_num2,data2['test'], deg = order)
c3 = np.polyfit(list_feature_num2,data2['cross'], deg = order)
x_new = np.linspace(1, 20, 57)
# f_liner1 = np.polyval(c1, x_new)
# f_liner2 = np.polyval(c2, x_new)
f_liner3 = np.polyval(c3, x_new)
# plt.plot(x_new, f_liner1, label = '拟合曲线', color='b',linewidth = 2,linestyle='-', marker='')
# plt.plot(x_new, f_liner2, label = '拟合曲线', color='orange',linewidth = 2,linestyle='-', marker='')
# plt.plot(x_new, f_liner3, label = '拟合曲线', color='r',linewidth = 2,linestyle='-', marker='')
plt.axvline(9, ymin = 0,  ymax = 0.72, linestyle="--", linewidth = 1, color = 'b') #画垂直线

# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)
plt.xlabel(u"descriptors num", font1)
plt.ylabel(u"cross validation accuracy", font1)
plt.grid(True, linestyle = "-.")


plt.show()