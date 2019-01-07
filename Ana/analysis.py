#--coding:utf-8--
import json
import numpy as np
from collections import defaultdict
import igraph
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
with open('/Users/xutao/Downloads/Python/data_set/phonedata/安徽移动.json','r') as f:
    ahmobile = json.load(f)
data_list = ahmobile['data']['data_list']
#print data_list
calls = data_list[0]['calls']
print calls
init_type = []
use_time = []
other_cell_phone = []
cell_phone = []
start_time=[]
for call in calls:
    init_type.append(call['init_type']) #呼叫类型
    use_time.append(call['use_time'])#通话时长
    other_cell_phone.append(call['other_cell_phone']) #对方号码
    cell_phone.append(call['cell_phone'])#本机号码？每个文件这个号码都一样
    start_time.append(call['start_time'])  #将通话开始时间加入
#print len(calls) #len=239
#for i in range(0,len(calls)): #测试用
    #print start_time[i]
import time
start_hour=[]  #存放日期中的小时
start_min=[] #存放分钟
start_hm=[] #存放具体时间几点几分
start_date=[]  #存放日期-day
for i in range(len(calls)):
    start_time[i]=time.strptime(start_time[i], "%Y-%m-%d %H:%M:%S")  #将日期字符串转换为日期格式
    #print start_time[i] #测试用
    start_hour.append(start_time[i].tm_hour)  #提取出时间中的小时
    start_min.append(start_time[i].tm_min) #提取出分钟
    start_date.append(start_time[i].tm_mday) #提取日期
    #print start_min[i]
    start_hm.append(float(start_hour[i])+float(1.0*start_min[i]/60)) 
#print start_hm
#检查other_phone_call中的不同电话号码数：
count=0
i=0
dic={}
dic_relation={}#存放计算的相关性数值
for item in other_cell_phone:
    if(item in dic.keys()):
        dic[item]+=1
        dic_relation[item]+=float(1.0*use_time[i]/max(use_time)) #用通话时长作为亲密度的衡量指标
    else:
        dic[item]=1
        dic_relation[item]=float(1.0*use_time[i]/max(use_time))
    i+=1
#print dic
#print dic_relation.values()
dic_num=[] 
for i in range(len(dic_relation.values())):
    dic_num.append(dic_relation.values()[i])
print dic_num
#print max(zip(dic_relation.values(),dic_relation.keys()))

from sklearn.cluster import KMeans
#kmeans.fit(start_hour)
call_information=[]
#合并成二维矩阵:通话时长+对方号码+通话起始时间小时
call_information = call_information  + [use_time] + [other_cell_phone] +[start_hour]
#print call_information
#统计每个时间段内的通话次数:
min_hour=min(start_hour)  #最早通话时间
max_hour=max(start_hour)  #最晚通话时间
#print min_hour,max_hour #测试用
cal_times=np.zeros(24) #创建统计通话次数的数组
cal_day=np.zeros(32) #统计每天的通话数
cal_usetime=np.zeros(24) #统计每小时通话时长
for i in range(len(calls)):
    hour=start_hour[i]
    day=start_date[i]
    time=use_time[i]
    cal_times[hour]+=1
    cal_day[day]+=1
    cal_usetime[hour]+=time
#print cal_usetime#测试用
#每个小时段的通话频次：
#x1=np.arange(min_hour,max_hour,1)
#plt.plot(x1,cal_times[x1],linewidth=1,color='blue',marker='*', markerfacecolor='r',markersize=8)
#plt.xlabel('Time by hour') 
#plt.ylabel('Num of phone call') 
#plt.title('Anhui Mobile Phone call by time') 
#plt.show()

#每天的通话频次：
#x2=np.arange(1,31,1)
#plt.plot(x2,cal_day[x2],linewidth=1,color='r',marker='*', markerfacecolor='green',markersize=8)
#plt.xlabel('Time by day') 
#plt.ylabel('Num of phone call') 
#plt.title('Anhui Mobile Phone call by day') 
#plt.show()

#每个小时段的通话时长：
#x3=np.arange(min_hour,max_hour,1)
#plt.plot(x3,cal_usetime[x3],linewidth=1,color='blue',marker='*', markerfacecolor='r',markersize=8)
#plt.xlabel('Usetime by hour') 
#plt.ylabel('UseTime') 
#plt.title('Anhui Mobile Phone call by time') 
#plt.show()

#合并通话时长和通话频率在一张图中：
def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.values():
        sp.set_visible(False)
fig, host = plt.subplots()
fig.subplots_adjust(right=0.75)
par1 = host.twinx()
t3 = np.arange(min_hour,max_hour,1)
p1, = host.plot(t3, cal_times[t3], linewidth=1,color='r',marker='o', markerfacecolor='green',markersize=8, label="call time")
p2, = par1.plot(t3, cal_usetime[t3],linewidth=1, color='blue',marker='+', markerfacecolor='green',markersize=8, label="use time")
host.set_xlim(min_hour,max_hour)
host.set_xlabel("Time by hour")
host.set_title("Use time & Call time by hour")
host.set_ylabel("Call time")
par1.set_ylabel("Use time")
host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1.get_color(), **tkw)
par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
host.tick_params(axis='x', **tkw)
lines = [p1, p2]
host.legend(lines, [l.get_label() for l in lines])
plt.show()


#绘制通话时长和通话时间段的散点图：
f1=plt.figure(1)
plt.scatter(start_hm,use_time,s=10)
plt.xlabel("time by hour")
plt.ylabel("use_time")
plt.title("scatter of use_time & call time")
plt.show()


import networkx as nx
N = 150
r = 2 * np.random.rand(N)
theta = 2 * np.pi * np.random.rand(N)
area = 200 * r**2
colors = theta
ax = plt.subplot(111, projection='polar')
c = ax.scatter(theta, r, c=colors, s=area, cmap='hsv', alpha=0.75)
plt.show()

#用通话时长和通话时间 构成二维样本,进行聚类
X = np.array(list(zip(start_hm,use_time))).reshape(len(start_hm), 2)
print X
for k in range(2,10):
    clf = KMeans(n_clusters=k) #设定k
    s = clf.fit(X) #加载数据集合
    numSamples = len(X) 
    centroids = clf.labels_
    print centroids,type(centroids) #显示中心点
    print clf.inertia_  #显示聚类效果
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    #画出所有样例点 属于同一分类的绘制同样的颜色
    for i in xrange(numSamples):
        #markIndex = int(clusterAssment[i, 0])
        plt.plot(X[i][0], X[i][1], mark[clf.labels_[i]],markersize=4) #mark[markIndex])
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
        # 画出质点，用特殊图型
    centroids =  clf.cluster_centers_
    for i in range(k):
        plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize = 8)
            #print centroids[i, 0], centroids[i, 1]
    plt.title("k=%d"%k)
    plt.show()

