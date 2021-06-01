import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
#原始14个特征：
names = ['alloy','class','$\delta$','$\Delta{H_{mix}}$','$\Delta{S_{mix}}$','Fi','RMS','VEC','r','Sc','$\Delta{H_{mix}^{ijmax}}$','$\Delta{H_{mix}^{ijmin}}$','$\sqrt{\delta{H_{mix}}}$','$\sqrt{\delta{H_{mix}^{0}}}$','$\sqrt{\delta{H_{mix}^{0+}}}$','$\sqrt{\delta{H_{mix}^{0-}}}$']
# names = ['1','2','d1','d2','d3','d4','d5','d6','d7','d8','d9','d10','d11','d12','d13','d14',]
data = pd.read_csv('/Users/xutao/Downloads/HEA-data/合并数据集-去除重复.csv',header=0,names = names)
x_tmp = data[names[2:]]

#去除5个相关性特征后的9个特征：
# names2 = ['alloy','class','Hmix','Smix','Fi','VEC','r','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0+']
# data = pd.read_csv('/home/xutao/Downloads/Python/HEA-data/合并数据集-去除重复-3-1-去除相关性数据-更改列名.csv',header=0,names = names2)
# x_tmp = data[names2[2:]]

#相关性范例数据
# name1 = ['alloy','class','x1','x2','x3','x4','x5']
# data = pd.read_csv('/home/xutao/Downloads/Python/HEA-data/相关性范例数据.csv',header=0, names =name1)
# x_tmp = data[name1[2:]]
# print(x_tmp.shape)

data = x_tmp.corr()
mask = np.array(data)
# mask = np.zeros_like(data_)
mask[np.triu_indices_from(mask)] = False#triu 上三角，tril 下三角；
#with sns.axes_style("white"):
#建立画板
fig=plt.figure()
#建立画纸 GnBu  vlag_r
ax1=fig.add_subplot(1,1,1)
sns.heatmap(data, annot = True,  vmin = -1, vmax = 1, mask = mask, cmap = "vlag_r",cbar_kws = dict(use_gridspec=False,location = "left"))
ax1.xaxis.tick_top()
ax1.yaxis.tick_right()
ax1.set_yticklabels(ax1.get_yticklabels(),rotation = 0) #y轴字体调整为水平
plt.show()