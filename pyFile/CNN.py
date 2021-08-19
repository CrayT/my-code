#第一步，很简单，导入MNIST数据集，创建默认的Interactive Session
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf

# mnist = tf.keras.datasets.mnist #tensorflow.examples.tutorials is now deprecated and it is recommended to use this.

mnist = input_data.read_data_sets("MNIST_data", one_hot = True)
sess = tf.InteractiveSession()
#定义权重和偏差的初始化函数，这样省得后来一遍遍定义，直接调用初始化函数就可以了。
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.1) #符合标准正太分布的随机值。
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.1, shape = shape) #返回形状为shape、值为0.1的常数tensor。
    return tf.Variable(initial)

#定义卷积层和池化层
def conv2d(x, W): #W是卷积核：[卷积核高度，宽度，输入通道，输出通道数]，输出通道数表示从上一层提取多少特征。
    return tf.nn.conv2d(x, W, strides = [1, 1, 1, 1], padding = 'SAME')

def max_pool_2_2(x): #ksize中间两个参数为池化窗口，第一与第四个是batch和channels池化大小，一般为1，与strides一样。
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = 'SAME') #SAME填充0，使输入输出保持大小一致；VALID不填充。

'''
定义输入的placeholder，x是特征，y_是真实的label。因为卷积神经网络是会用到2D的空间信息，
所以要把784维的数据恢复成28*28的结构，使用的函数就是tf.shape的函数。
卷积核的输出通道数：一般采用16的倍数，并且随着层级增加增大。out_channel是一个非常自由的参数，也比较重要。
个人理解是，每一个池化层都是将tensor缩并的过程，其作用是将图片分块，提炼出关键信息。
这其中必然损失图像或者数据的大量信息，因此为了减少池化过程中的信息损失，增加卷积核数量。
增加卷积核可以将图片或者数据信息从不同的角度进行分块、信息提炼。
'''
x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])
x_image = tf.reshape(x, [-1, 28, 28, 1]) #将输入x变成28*28结构，[batch,高度，宽度，输入通道]。

#第一个卷积层
W_conv1 = weight_variable([5, 5, 1, 32]) #卷积核：[高度，宽度，输入通道，输出通道数]
b_conv1 = bias_variable([32])
h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2_2(h_conv1) #pooling之后，输出长*宽：14*14，输出通道32.

#第二个卷积层
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])
h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2_2(h_conv2) #pooling之后，输出长*宽：7*7，输出通道64.

#定义第一个全连接层，输出为1024维的向量
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64]) #长*宽：7*7，通道数64.
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1) #Relu整流。

# 使用Dropout，keep_prob初始化时是一个占位符，训练时为0.5，测试时为1
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

#最后一个输出层也要对权重和偏差进行初始化。
W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

#定义损失函数和训练的步骤，使用Adam优化器最小化损失函数。
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices = [1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

#计算预测的精确度。tf.reduce_mean用于计算tensor沿着指定的轴的平均值。
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1)) #argmax(input, axis),axis为1返回每行最大值索引。
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32)) #tf.cast用于改变tensor的数据类型。

'''
对全局的变量进行初始化，迭代20000次训练,使用的minibatch为50，所以总共训练的样本数量为100万。
'''
tf.global_variables_initializer().run()
for i in range(20000):
    batch = mnist.train.next_batch(50)
    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict = {x: batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g"%(i, train_accuracy))
    train_step.run(feed_dict = {x: batch[0], y_: batch[1], keep_prob: 0.5})

#输出最后的准确率。
print("test accuracy %g"%accuracy.eval(feed_dict = {x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))