#--coding:utf-8--
import json
import numpy as np
import pandas as pd
import pinyin
import time
from collections import defaultdict
import matplotlib
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from datetime import datetime,date
#address="/Users/xutao/Downloads/Python/data_set/phonedata的副本/运营商数据" #MAC 定义文件地址，下面代码会调用。
address="/Users/xutao/Downloads/Python/data_set/phonedata/移动通话详单采集结果2" 
#address="/home/xutao/Downloads/Python/data_set/phonedata的副本/运营商数据"  #实验室
with open(address+'.json','r') as f: #ubuntu
    ahmobile = json.load(f)
#data_list = ahmobile['data']['data_list']
data_list=ahmobile['data']['data_list']
#print data_list
#calls = data_list[0]['calls']
calls=data_list
#print calls
init_type = [] #呼叫类型：主叫、被叫
use_time = []
other_cell_phone = []
cell_phone = []
start_time=[]
place=[]
cell_phone.append(calls[0]['phone'])
print "本机号码:",cell_phone[0]
def time2se(t): #转换时间
    h,m,s = t.strip().split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)
for call in calls:
    #print call['call_type']
    if(call['call_duration']and call['opposite_phone']and call['begin_time']and call['call_type']):
        #if('\u4e3b\u53eb' in call['call_type'].decode('utf-8')):  #二值化主叫被叫，主叫为1，被叫为0
            #init_type.append(1)   
       # else:
            #init_type.append(0)
        #init_type.append(call['init_type']) #呼叫类型
        use_time.append(time2se(call['call_duration']))#通话时长
        other_cell_phone.append(call['opposite_phone']) #对方号码
       # cell_phone.append(call['cell_phone'])#本机号码
        start_time.append(call['begin_time'])  #将通话开始时间加入
        if(call['calling_city']):
            place.append(pinyin.get(call['calling_city'], format="strip", delimiter=""))#地点转换为字符串后存储
        else:
            place.append('Na')
#print len(start_time) #len=1173,即有效数据
#for i in range(0,len(calls)): #测试用
    #print start_time[i]
#print max(use_time)
start_hour=[]  #存放日期中的小时
start_min=[] #存放分钟
start_hm=[] #存放具体时间几点几分
start_date=[]  #存放日-day
start_date1=[] #存放月日,比如10月2号，以10.02数字存放
start_weekday=[] #存放星期几
i=0
for item in start_time:
#for i in range(len(calls)):
    start_weekday.append(datetime.strptime(item, "%Y-%m-%d %H:%M:%S").weekday()+1) #将日期转换为星期
    item=time.strptime(item, "%Y-%m-%d %H:%M:%S")  #将日期字符串转换为日期格式
    #item2=time.strptime(item,"%Y-%m-%d")
    #rint item1#测试用
    start_hour.append(item.tm_hour)  #提取出时间中的小时
    start_min.append(item.tm_min) #提取出分钟
    start_date.append(item.tm_mday) #提取日期
    start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
    #start_year_day.append(item.tm_year,item.tm_mon,item.tm_mday)
    #print start_min[i]
    start_hm.append(float(start_hour[i])+float(1.0*start_min[i]/60)) 
    i+=1
#print start_date1
#用day_count统计记录中出现的日期，每个日期只记录一次
day_count=[]
for item in start_date1:
    if(item in day_count):
        pass
    else:
        day_count.append(item)
print "记录中出现天数：",len(day_count)  #打印出日期天数
#统计每个时间段内的通话次数:
min_hour=min(start_hour)  #最早通话时间
max_hour=max(start_hour)  #最晚通话时间
#print min_hour,max_hour #测试用
cal_times=np.zeros(24) #创建统计通话次数的数组
cal_day=np.zeros(32) #统计每天的通话数
cal_usetime=np.zeros(24) #统计每小时通话时长
for i in range(len(start_date)):
    hour=start_hour[i]
    day=start_date[i]
    time=use_time[i]
    cal_times[hour]+=1
    cal_day[day]+=1
    cal_usetime[hour]+=time
#print cal_usetime#测试用
#检查other_phone_call中的不同电话号码数：
count=0
dic={} #字典，存放号码和对应次数
dic_relation={}#存放计算的相关性数值
def dic_relation():
    i=0
    for item in other_cell_phone:
        if(item in dic.keys()):
            dic[item]+=1
            #dic_relation[item]+=float(1.0*use_time[i]/max(use_time))+float(1.0*init_type[i]/100)+float(1.0/100)#用通话时长作为亲密度的衡量指标
        else:
            dic[item]=1
            #dic_relation[item]=float(1.0*use_time[i]/max(use_time))
        i+=1
#max_call_time= max(dic.values())
dic_relation()
#print dic
#print len(dic)
#print start_date
#建立词典，一个号码若每天都打电话，则标记为1，否则标记为比例：
dic_phone_day={}
dic_phone_work={}#统计工作日天数
dic_phone_fev={}#节假日
#先讲全部置一。
for item in other_cell_phone:
    if(item in dic_phone_day.keys()):
        pass
    elif(item in dic_phone_work.keys()):
        pass
    elif(item in dic_phone_fev.keys()):
        pass
    else:
        dic_phone_day[item]=1
        dic_phone_work[item]=1
        dic_phone_fev[item]=1
#统计每个号码的工作日电话数
i=0
for item in dic_phone_work.keys():
    i=0
    j=0
    f=0
    for call in other_cell_phone:
        if (item==call):
            if(start_weekday[i]>=1 and start_weekday[i]<=5):
                j+=1
            elif(start_weekday[i]>=6 and start_weekday[i]<=7):
                f+=1
            else:
                pass
        else:
            pass
        i+=1
    dic_phone_work[item]=j
    dic_phone_fev[item]=f
#print dic_phone_fev     #测试
#print dic_phone_work  
dic_phone_ratio={} #存放通话通话比例
def input_mm():#自定义输入上下限
    global Min
    Min=input("请输入双休-工作日通话次数比例下限(-1~+1):") 
    if Min<-1 or Min >1:
        print "最小值输入错误，请重新输入:"
        return input_mm()
    global Max
    Max=input("请输入双休-工作日通话次数比例上限(-1~+1):")
    if Max<-1 or Max >1:
        print "最大值输入错误，请重新输入:"
        return input_mm()  
    if Min>=Max:
        print "最小值大于最大值，请重新输入:"  
        return input_mm()
input_mm()
for item in dic_phone_day.keys():
    if item in dic_phone_ratio.keys():
        pass
    else:
        dic_phone_ratio[item]=float(1.0*(dic_phone_fev[item]-dic_phone_work[item])/(dic_phone_fev[item]+dic_phone_work[item]))
#print dic_phone_ratio
#print Min,Max #测试
dic_phone_select={}#建立根据比例筛选出的号码词典：
for item in dic_phone_ratio.keys():
    if (dic_phone_ratio[item]>=float(Min) and dic_phone_ratio[item]<=float(Max) and dic[item]>(len(day_count))/10):
        dic_phone_select[item]=dic_phone_ratio[item]
print "按照节假日-工作日通话比例排序后："
for item in sorted(dic_phone_select.iteritems(), key = lambda asd:asd[1], reverse=True) :
    print item  #按照从大到小排序输出
#如下代码作用：统计出所有号码通话天数，即若某天有通话(无论一天中通话多少次)，则加一，
for item in dic_phone_day.keys():
    j=0
    tmp=[]
    for call in other_cell_phone:
        #print call
        if (item!=call):
            pass
            j+=1
        else:                                                                                                                                  
            if(start_date1[j] in tmp):
                pass
            else:
                tmp.append(start_date1[j])
            j+=1
    dic_phone_day[item]=len(tmp)
print "最多通话天数：",max(dic_phone_day.values())
most_related_num=max(dic_phone_day.items(),key=lambda x:x[1])[0]
print "最多通话天数号码:",most_related_num
#统计每个号码打电话天数：
phone_calldays=[] #作为记录
for i in range(len(other_cell_phone)):
    if(other_cell_phone[i]in dic_phone_day.keys()):
        phone_calldays.append(dic_phone_day[str(other_cell_phone[i])])
    else:
        print 'error',other_cell_phone[i]   
    i+=1

#排名前十的号码中有8个出现在之前定义的Top10中
dic_phone_day_array=[]
#按照通话天数进行排序dataframe.to_csv("/home/xutao/Downloads/test.csv",index=True,sep=',',columns=columns,encoding='utf-8')
dic_phone_day_sort=sorted(dic_phone_day.iteritems(), key = lambda asd:asd[1], reverse=True)
#print dic_phone_day_sort
for item in dic_phone_day_sort:
    dic_phone_day_array.append(item[0])   
dic_phone_day_top10=dic_phone_day_array[0:10] #取前十
#print dic_phone_day_sort      
#print dic_phone_day
#print len(start_date)  #1173 
#print max_call_time #159

def dic_relation2():
#按照关系的键值从大到小进行排序
    dic_relation_sort=sorted(dic_relation.iteritems(), key = lambda asd:asd[1], reverse=True)
#print dic_relation_sort

    dic_name=[] #存放号码
    dic_relation=[] #存放关系值
    for item in dic_relation_sort:
    #print item
        dic_name.append(item[0])
        dic_relation.append(item[1])
    dic_name1=dic_name[0:10]  #取前10的电话号码
    dic_name2=dic_name[0:50]
    dic_relation1=dic_relation[0:10]

weekday={  #转换星期
    1:'星期一',
    2:'星期二',
    3:'星期三',
    4:'星期四',
    5:'星期五',
    6:'星期六',
    7:'星期日',
}
relation=[] #标记关系
w=0
p=0
o=0
#rawdata1=pd.read_csv('/Users/xutao/Desktop/副本 通话详单采集1.csv') #MAC
#rawdata11=[] #写入数组中
#for i in range(len(rawdata1)):
 #   rawdata11.append(rawdata1['other_cell_phone'][i])
#print rawdata11 #测试
print "筛选出的号码通话记录:"
tmparray=[]
for i in range(len(other_cell_phone)):
    
    if(other_cell_phone[i]==most_related_num):
        relation.append('1') #wife
        w+=1
     #将符合父母条件的打标记
    elif(start_hour[i]>=17 and start_hour[i]<=22 and use_time[i]>120  and start_weekday[i]>=5 and start_weekday[i]<=7): #and len(other_cell_phone[i])>8 )# and other_cell_phone[i][0]!='0'): #过滤掉0开始的号码):
        relation.append('2') #family
        if(other_cell_phone[i] in dic_phone_select.keys()):  
            print other_cell_phone[i],":通话开始时间:",start_hour[i],"点, 通话时长:",use_time[i],"s, 星期几通话:",weekday[start_weekday[i]],", 通话日期:",start_date1[i],"号"
            if(other_cell_phone[i] in tmparray):
                pass
            else:
                tmparray.append(other_cell_phone[i])
        p+=1
    #elif(other_cell_phone[i]=='13852882991'): #输出某个号码的通话记录
        #print other_cell_phone[i],":通话开始时间:",start_hour[i],"点, 通话时长:",use_time[i],"s, 星期几通话:",weekday[start_weekday[i]],", 通话日期:",start_date1[i],"号,location:",place[i]
    else:
        relation.append('0') #其他
        o+=1
print "筛选出的号码为:"
print "1 :",most_related_num
i=0
for item in sorted(dic_phone_select.iteritems(), key = lambda asd:asd[1], reverse=True):
    if item[0] in tmparray:
        print i+2,":",item[0]
        i+=1
    else:
        pass
#print dic_phone_day_regular18811472815
#print "len(wife):",w
#print "len(parent):",p
#print "len(other):",o
festival={
    1.01:'元旦',
    1.05:'腊八节',
    1.15:'元宵',
    2.14:'情人节',
    4.04:'清明',
    5.01:'劳动节',
    5.05:'端午节',
    6.1:'',
    8.15:'中秋节',
    10.01:'国庆节',
    11.05:'冬至',
    12.3:'除夕',
    12.25:'圣诞节',
}
#以下代码统计other_cell_phone的归属地：
def data_to_csv():
    from phone import Phone
    p = Phone()
    phone_place=[]
    phones =other_cell_phone
    for phone in phones:
        if(phone[0]=='1'): #手机号1开头，并且11位
            if len(phone)==11: 
                city = p.find(phone)['city']
                phone_place.append(pinyin.get(city, format="strip", delimiter="")) #同时将地名转换为字符串
                #phone_place.append(city)
            else:
                phone_place.append('Na')
        else:
            phone_place.append('Na') #不是手机号的话置Na
    festival_array=[] #节日列表
    #print start_date1
    for item in start_date1:
        if(item in festival.keys()):
            festival_array.append(festival[item])
        else:
            festival_array.append('Na') #其他
    #print len(other_cell_phone)
    #print len(start_weekday)
    #print len(start_hour)
    #print len(use_time)
    #print len(start_date1)
    #print len(place)
    #print len(phone_place)
    #print len(phone_calldays)
    #根据已有数组创建csv文件
    columns=['phone_num','weekday','start_hour','use_time','start_date','location','other_phone_place','call_days']
    dataframe=pd.DataFrame({'phone_num':other_cell_phone,'weekday':start_weekday,'start_hour':start_hour,'use_time':use_time,'start_date':start_date1,'location':place,'other_phone_place':phone_place,'call_days':phone_calldays})
    dataframe.to_csv(address+'.csv',index=True,sep=',',columns=columns,encoding='utf-8') #默认写模式


def print_num():
    import csv
    with open(address+'.csv','rb') as myFile:  
        lines=csv.reader(myFile)  
        for line in lines:  
            if(line[1]=='18616002411'):
                print line
#先筛选出符合条件的号码：
def plot_screen_num():
    i=0
    for i in range(len(other_cell_phone)):
        #将符合父母条件的打标记
        if(start_hour[i]>=18 and start_hour[i]<=22 and use_time[i]>60 and use_time[i]<600 and start_weekday[i]>=5 
        and start_weekday[i]<=6 and len(other_cell_phone[i])>8 and other_cell_phone[i][0]!='0' #过滤掉0开始的号码
        and init_type[i]==1 ):
            print other_cell_phone[i],":通话开始时间:",start_hour[i],"点, 通话时长:",use_time[i],"s, 星期几通话:",weekday[start_weekday[i]],", 通话日期:",start_date[i],"号",
            proba_parent.append(1)#将该号码标记为父母，标记为1
            if(init_type[i]):
                print ", 通话方式:","主叫"
            else:
                print ", 通话方式:","被叫"
            
        else:
            proba_parent.append(0) #标记为其他，以0标记
        i+=1
#输出所有号码信息,这个函数的调用需要在plot_screen_num调用后才行。
def plot_rela():
    i=0
    for i in range(len(other_cell_phone)):
        if(start_hour[i] and use_time[i]):
            print other_cell_phone[i],":通话开始时间:",start_hour[i],"点, 通话时长:",use_time[i],"s, 星期几通话:",weekday[start_weekday[i]],", 通话日期:",start_date[i],"号",
            if(proba_parent[i]):
                print ", 该号码可能为家人。"
            else:
                print ", 该号码可能为其他。"
        i+=1
#画出排名关系值前十的电话
def plot_top10():  
    x = range(len(dic_name1))
    y = dic_relation1
    plt.plot(x, y, '--*')
    plt.xticks(x, dic_name1, rotation=30)
    plt.margins(0.08)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel("partial relation")
    plt.title("Top 10 phone num by relation")
    plt.show()

from sklearn.cluster import KMeans
#每个小时段的通话频次：
def call_timebyHour():
    x1=np.arange(min_hour,max_hour,1)
    plt.plot(x1,cal_times[x1],linewidth=1,color='blue',marker='*', markerfacecolor='r',markersize=8)
    plt.xlabel('Time by hour') 
    plt.ylabel('Num of phone call') 
    plt.title('Anhui Mobile Phone call by time') 
    plt.show()

#每天的通话频次：
def call_timebyDay():
    x2=np.arange(1,31,1)
    plt.plot(x2,cal_day[x2],linewidth=1,color='r',marker='*', markerfacecolor='green',markersize=8)
    plt.xlabel('Time by day') 
    plt.ylabel('Num of phone call') 
    plt.title('Anhui Mobile Phone call by day') 
    plt.show()

#每个小时段的通话时长：
def use_timebyHour():
    x3=np.arange(min_hour,max_hour,1)
    plt.plot(x3,cal_usetime[x3],linewidth=1,color='blue',marker='*', markerfacecolor='r',markersize=8)
    plt.xlabel('Usetime by hour') 
    plt.ylabel('UseTime') 
    plt.title('Anhui Mobile Phone call by time') 
    plt.show()

#合并通话时长和通话频率在一张图中：
def use_time_fre():
    fig, host = plt.subplots()
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
def use_time_hour():
    f1=plt.figure(1)
    plt.scatter(start_hm,use_time,s=10)
    plt.xlabel("time by hour")
    plt.ylabel("use_time")
    plt.title("scatter of use_time & call time")
    plt.show()

#Kmeans聚类：
def _Kmeans():
    start_hm_tmp=[]
    use_time_tmp=[]
#print max(use_time),min(use_time) #max=3534
    for item in start_hm:
        start_hm_tmp.append(float(1.0*item/10))
    for item in use_time:
        use_time_tmp.append(float(1.0*item/100))
    #print use_time_tmp
    #print start_hm_tmp
#用通话时长和通话时间 构成二维样本,进行聚类
    X = np.array(list(zip(start_hm_tmp,use_time_tmp,init_type))).reshape(len(start_hm), 3)
    #print X
    for k in range(3,4):
        clf = KMeans(n_clusters=k) #设定k
        s = clf.fit(X) #加载数据集合
        numSamples = len(X) 
        centroids = clf.labels_
        #print centroids,type(centroids) #显示中心点
        #print clf.inertia_  #显示聚类效果
        mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    #画出所有样例点 属于同一分类的绘制同样的颜色
        for i in xrange(numSamples):
        #markIndex = int(clusterAssment[i, 0])
            plt.plot(X[i][0]*10, X[i][1], mark[clf.labels_[i]],markersize=4) #mark[markIndex])
        mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
        # 画出质点，用特殊图型
        centroids =  clf.cluster_centers_
        for i in range(k):
            plt.plot(centroids[i][0], centroids[i][1], mark[i], markersize = 8)
            #print centroids[i, 0], centroids[i, 1]
        plt.xlabel("time by hour")
        plt.ylabel("use_time")
        plt.title("k=%d"%k)
        plt.show()
#igraph OK！！！
#from igraph import *  
#g = Graph.Famous("petersen")  
#plot(g)  
#print dic_relation1
from igraph import *
def relationi_net():
    import igraph
    count_fans=len(dic_name2)      
    count_following=len(dic_phone_day_top10)       
    #print count_fans  
    #print count_following  
    dic_name20=dic_name2           #与其相关号码，取前50
    top10=dic_phone_day_top10        #Top10号码
    g = Graph()          #创建
    g.add_vertices(3+count_fans+count_following) #添加节点，多了三个中心节点
    g.add_edges([(0,1),(1,2)]) #添加边
    g.vs[0]["name"]='Record'  
    g.vs[1]["name"]=cell_phone[0] #机主号码
    g.vs[2]["name"]='Top10' 
    g.es["trunk"] = [True, True]
    #g.es["weights"]=dic_relation #设置weights无用，无法控制边长。
    g.vs["main_node"]=[3,5.5,3]  #调节中心节点大小
    for i in range(3,count_fans+3):
      g.add_edges([(0,i)])
      g.es[i-1]["trunk"]=False
    for j in range(count_fans+3,3+count_fans+count_following):
        g.add_edges([(2,j)])
        g.es[j-1]["trunk"]=False
    index=3
    for name in dic_name20:
        g.vs[index]["name"]=name
        #g.es["weights"]=dic_relation
        g.vs[index]["main_node"]=False
        index+=1
    for name in top10:
        g.vs[index]["name"]=name
        g.vs[index]["main_node"]=False
        index+=1
        i+=1
    visual_style = {}
    color_dic={3:"#32CD32",5.5:"#FF8C00",False:"#76EEC6"}
    color_dic1={2.0:"#321232",3:"#4156E1",False:"#7B12EE"}
    visual_style["vertex_label_size"]=10 #每个叶节点字符大小、
    visual_style["vertex_label_color"]="#000000" #字符颜色
    visual_style["vertex_label_dist"]=0 #字符与节点距离
    visual_style["vertex_shape"]="circle"
    visual_style["vertex_size"] = [15+ 10*int(main_node) for main_node in g.vs["main_node"]] #叶节点大小
    visual_style["edge_width"] = [1 + 2 * int(trunk) for trunk in g.es["trunk"]]
    visual_style["vertex_color"] =[color_dic[main_node] for main_node in g.vs["main_node"]]
    visual_style["vertex_label"] = g.vs["name"]
    visual_style["bbox"] = (1000, 1000)
    visual_style["margin"] = 100  #缩放整个网，值越大越小
    #layout = g.layout("grid_fr")
    layout = g.layout("large")
    #layout=g.layout_grid_fruchterman_reingold
    visual_style["layout"] = layout
    plot(g, **visual_style)
