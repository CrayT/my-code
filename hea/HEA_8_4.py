#coding:utf8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/小论文/数据/9个特征重要性排序-4-3.csv',header=0)
print(data.shape)
print(data.columns.values.tolist())

acc_ = list(data['acc'])
print(acc_)
acc = list(reversed(acc_))
print(acc)
#希腊字符转义：
#fea = ['$\Delta{H_{mix}}$', '$\Delta{S_{mix}}$', 'Fi', 'r', '$\Delta{H_{mix}^{ijmax}}$', 'VEC', '$\Delta{H_{mix}^{ijmin}}$', '$\sqrt{\delta{H_{mix}}}$', '$\sqrt{\delta{H_{mix}^{0+}}}$']
fea= ['VEC','$\sqrt{\delta{H_{mix}^{0+}}}$', '$\Delta{H_{mix}}$','$\sqrt{\delta{H_{mix}}}$', '$\Delta{H_{mix}^{ijmax}}$', '$\Delta{H_{mix}^{ijmin}}$','Fi', 'r', '$\Delta{S_{mix}}$']
fea_ = fea.copy()
fea = list(reversed(fea_))
print(fea)
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

# plt.subplot(1,2,1)
# plt.barh(fea, acc, height = 0.8, align='center', color='#1E90FF', tick_label = fea)
# plt.xlim(0.6, 0.8)
# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)
# plt.xlabel(u"accuracy", font1)
# plt.ylabel(u"descriptor", font1)
# plt.grid(True, linestyle = "-.")

# plt.subplot(1,2,2) # yerr = 0.01, capsize = 10, ecolor = 'r' ,
yerr = []
for item in list(reversed(acc)):
    yerr.append((1-item)/7.15447154)
ecolor = ['g','r','r','r','r','r','r','r','r']
capsize = [10 for i in range(9)]
plt.bar(list(reversed(fea)), list(reversed(acc)),  width = 1, edgecolor = 'black', lw = 1.5, align='center', color='#156be5', tick_label = list(reversed(fea)))
plt.ylim(0.6, 0.8)
plt.xlabel(u"descriptor", font1)
plt.ylabel(u"accuracy", font1)
plt.grid(True, linestyle = "-.")

plt.show()