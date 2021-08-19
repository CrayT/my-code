import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd
names=['alloy','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']
data=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/合并数据集-去除重复.csv',header=0,names=names)
y=data[["class"]]
# X=pd.read_csv('/home/xutao/Downloads/Python/HEA-data/generate_feature_1120.csv')
X=data[names[2:]]
# print(X.shape,y)
# print(y,type(y))



def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 1,dtype=np.float64)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape,dtype=np.float64)
    return tf.Variable(initial)

graph=tf.Graph()
with graph.as_default():
    x = tf.placeholder(tf.float64, shape=(None, 14))
    y_= tf.placeholder(tf.float64, shape=(None, 1))

    tf_labels=tf.constant(y)

    #隐藏层1：
    hidden_w1=weight_variable([14,100]) #输入维度14,100个隐藏单元
    hidden_b1=bias_variable([100])
    #隐藏层2：
    hidden_w2=weight_variable([100,100]) #100个隐藏单元
    hidden_b2=bias_variable([100])
    #输出层：
    out_w=weight_variable([100,1]) #输出层5个类别
    out_b=bias_variable([1])

    #x*w1+b1
    layer1=tf.matmul(X,hidden_w1)#+hidden_b1
    layer1_=tf.nn.relu(layer1)

    #layer*w2+b2
    layer2=tf.matmul(layer1_,hidden_w2)#+hidden_b2
    layer2_=tf.nn.relu(layer2)

    #输出层：
    logits=tf.matmul(layer2_,out_w)#+out_b

    # L2正则化
    regularization = tf.nn.l2_loss(hidden_w1) + tf.nn.l2_loss(hidden_w2) + tf.nn.l2_loss(out_w)

    loss = tf.reduce_mean(
        tf.nn.softmax_cross_entropy_with_logits_v2(labels=tf_labels, logits=logits) + 0.001 * regularization)

    print("hello")

    optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

    print("world")

    train_prediction = tf.nn.softmax(logits)

    weights = [hidden_w1, hidden_b1, hidden_w2, hidden_b2, out_w, out_b]

num_steps = 5000

def accuracy(predictions, labels):
    # print(predictions)
    # print(labels)
    for 
    return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1)) / 407)

def relu(x):
    return np.maximum(0,x)
          
with tf.Session(graph=graph) as session:
    tf.global_variables_initializer().run()
    print('Initialized')
    for step in range(num_steps):
        _, l, predictions = session.run([optimizer, loss, train_prediction])
        # start=step*10%407
        # end=step*10%407+10
        # session.run(optimizer,feed_dict={x:X,y_:y})
        # print(predictions.shape)
        # print(predictions)
        if (step % 100 == 0):
            # total_cross_entropy = session.run(loss, feed_dict={x: X, y_: y})
            # print("After %d training step(s), cross entropy on all data is %g" % (step, total_cross_entropy))

            # print("accuracy: %.2f%%"%accuracy(predictions,labels))

            # print('Loss at step %d: %f' % (step, l))
            print('Training accuracy: %.1f%%' % accuracy(predictions, y['class']))
    
'''
    w1, b1, w2, b2, w3, b3 = weights
    # 显示分类器
    h = 0.02
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))

    Z = np.dot(relu(np.dot(relu(np.dot(np.c_[xx.ravel(), yy.ravel()], w1.eval()) + b1.eval()), w2.eval()) + b2.eval()), w3.eval()) + b3.eval()
    Z = np.argmax(Z, axis=1)
    Z = Z.reshape(xx.shape)
    fig = plt.figure()
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap=plt.cm.Spectral)
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
'''