import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']

X=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/corelation.csv')

x_tmp = X

print(x_tmp.shape)

data = x_tmp.corr()
sns.heatmap(data, annot = True, cmap = "GnBu")
plt.show()