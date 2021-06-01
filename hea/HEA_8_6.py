#coding:utf8
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/小论文/数据/6种算法交叉准确率5-25.csv',header=0)
print(data.shape)
print(data.columns.values.tolist())

acc = data['ACC']

ml = data['ml']

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

# 加粗边框
ax.spines['bottom'].set_linewidth(2)
ax.spines['left'].set_linewidth(2)
ax.spines['right'].set_linewidth(2)
ax.spines['top'].set_linewidth(2)

# ecolor = ['#1E90FF','#1E90FF','#1E90FF','#1E90FF','#1E90FF','#1E90FF','g']


N = 6
theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
radii = acc
width = np.pi / 4 * np.random.rand(N)

la = ['DTC', 'RFC', 'GBC', 'ABC', 'SVC', 'LR']
ax = plt.subplot(111, projection='polar')
bars = ax.bar(theta, radii, width = width, bottom=0.0, tick_label = la,)
for r, bar in zip(radii, bars):
    rr = r+np.random.rand(1)[0]

    bar.set_facecolor(plt.cm.viridis(rr/4))
    bar.set_alpha(0.9)

plt.show()