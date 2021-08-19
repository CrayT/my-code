#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split,cross_val_score
import os

'''
先运行代码，模型会保存在mymodels文件夹；
然后运行tensorboard --logdir=mymodels路径，即可访问tensorboard页面。
'''

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'#不然提示CPU问题。

names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0plus','rootHmix0neg']
data=pd.read_csv('/Users/xutao/Downloads/HEA_data/合并数据集-去除重复.csv',header=0,names=names)
y=data[["class"]]
X=data[names[2:]]

Y=y

for item in range(Y.shape[0]):
    Y.iloc[item,0]=Y.iloc[item,0]-1
    # print(Y.iloc[item,0])

x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.3, random_state=33)

my_feature_columns = []
for key in names[2:]:
    my_feature_columns.append(tf.feature_column.numeric_column(key=key))

dir_path='/Users/xutao/Downloads/Python/my-code/'
tf.logging.set_verbosity(tf.logging.INFO)
models_path=os.path.join(dir_path,'mymodels/')

classfier=tf.estimator.DNNClassifier(
    model_dir=models_path, #保存模型，便于tensorboard可视化。
    feature_columns=my_feature_columns,
    hidden_units=[100,100,100],
    n_classes=5
)

def train_func(train_x,train_y):
    dataset=tf.data.Dataset.from_tensor_slices((dict(train_x), train_y))
    dataset = dataset.shuffle(5000).repeat().batch(100)
    return dataset

classfier.train(
    input_fn=lambda:train_func(x_train,y_train),steps=1000)

def eval_input_fn(features, labels, batch_size):
    features=dict(features)
    if labels is None:
        # No labels, use only features.
        inputs = features
    else:
        inputs = (features, labels)
    dataset = tf.data.Dataset.from_tensor_slices(inputs)
 
    assert batch_size is not None, "batch_size must not be None"
    dataset = dataset.batch(batch_size)
    return dataset

predict_arr = []
predictions = classfier.predict(
        input_fn=lambda:eval_input_fn(x_test,labels=y_test,batch_size=100))

for predict in predictions:

    predict_arr.append(np.argmax(predict['probabilities']))

result = predict_arr == y_test
result=result.values #Dataframe转数组
result1 = [w for w in result if w == True]

print("准确率为 %s"%str((len(result1)/len(result))))
