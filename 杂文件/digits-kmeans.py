#--coding:utf-8--
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
digits_train=pd.read_csv("/home/xutao/Downloads/Python/data_set/optdigits/optdigits.tra",header=None)
digits_test=pd.read_csv("/home/xutao/Downloads/Python/data_set/optdigits/optdigits.tes",header=None)
#print digits_test  65个维度，最后一维是识别数字
x_train=digits_train[np.arange(64)]
#print x_train
y_train=digits_train[64]
x_test=digits_test[np.arange(64)]
y_test=digits_test[64]
from sklearn.cluster import KMeans
kmeans=KMeans(n_clusters=10) #10个聚类中心
kmeans.fit(x_train) #聚类不带标签的聚类
y_pred=kmeans.predict(x_test)
from sklearn import metrics
print metrics.adjusted_rand_score(y_test,y_pred)

