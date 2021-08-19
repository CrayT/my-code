import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']
data=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/合并数据集-去除重复.csv',header=0,names=names)
Y=data[["class"]]
X=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/corelation.csv')
x_tmp = X

x_tmp['class'] = np.array(Y['class'])
print(x_tmp.shape)

d = ["d1","d2","d3","d4","d5","d6","d7","d8"]

print(x_tmp.shape)

g = sns.pairplot (x_tmp,  size = 4, vars = d, hue="class", diag_kind = "hist")
plt.show()
