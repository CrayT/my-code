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
#定义特征列,每个 tf.feature_column 都标识了特征名称、特征类型和任何输入预处理操作。
for key in names[2:]:
    my_feature_columns.append(tf.feature_column.numeric_column(key=key))

<<<<<<< HEAD:NN-2.py
dir_path='/Users/xutao/Downloads/Python/my-code/'
=======

dir_path='/home/xutao/Downloads/Python/'
>>>>>>> a7ec5911efd28e89d399a129d7bb5367e6099ea0:pyFile/NN-2.py
tf.logging.set_verbosity(tf.logging.INFO)
models_path=os.path.join(dir_path,'mymodels/')

classfier=tf.estimator.DNNClassifier(
    model_dir=models_path, #保存模型，便于tensorboard可视化。
    feature_columns=my_feature_columns,
    hidden_units=[100,100,100],
    n_classes=5
)

def input_train(train_x,train_y): #训练集导入函数
    dataset=tf.data.Dataset.from_tensor_slices((dict(train_x), train_y))
    dataset = dataset.shuffle(100).repeat().batch(50)
    '''
    shuffle,数字越大，打乱数据的程度越大；
    batch，按照顺序取出指定数字的数据，最后一次可能小于batch；
    repeat，数据集重复了指定次数，
    '''
    return dataset
print(input_train(x_train,y_train))

classfier.train(
    input_fn=lambda:input_train(x_train,y_train),steps=500) #训练steps步停止

def eval_input_fn(features, labels, batch_size): #测试集导入函数
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

#评估模型：
eval_result=classfier.evaluate(
    input_fn=lambda:eval_input_fn(x_test,labels=y_test,batch_size=100)
)
print("\neval_result:%s"%(eval_result))
print("\nTest set accuracy: {accuracy:0.3f} \n".format(**eval_result))

#模型预测：
predict_arr = []
predictions = classfier.predict(
        input_fn=lambda:eval_input_fn(x_test,labels=y_test,batch_size=100))

for predict in predictions:
    #从prediction中得到概率最大的索引作为预测最终类别：
    predict_arr.append(np.argmax(predict['probabilities'])) 

result = predict_arr == y_test
result=result.values #Dataframe转数组
result1 = [w for w in result if w == True]

print("准确率为 %s"%str((len(result1)/len(result))))