#coding:utf-8
def select():
    start_hour=[]  #存放日期中的小时
    start_date=[]  #存放日-day
    start_date1=[] #存放月日,比如10月2号，以10.02数字存放
    start_weekday=[] #存放星期几
    for item in start_time:
#for i in range(len(calls)):
        if '/' in str(item): #判断日期格式
            if str(item).count('/')==2 and str(item).count(':')==2:
            #print "1"
                start_weekday.append(datetime.strptime(item, "%Y/%m/%d %H:%M:%S").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%Y/%m/%d %H:%M:%S")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
            elif str(item).count('/')==2 and str(item).count(':')==1:
            #print "2"
                start_weekday.append(datetime.strptime(item, "%Y/%m/%d %H:%M").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%Y/%m/%d %H:%M")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
            elif str(item).count('/')==1 and str(item).count(':')==2:
            #print "3"
                start_weekday.append(datetime.strptime(item, "%m/%d %H:%M:%S").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%m/%d %H:%M:%S")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
            elif str(item).count('/')==1 and str(item).count(':')==1:
                start_weekday.append(datetime.strptime(item, "%%m/%d %H:%M").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%m/%d %H:%M")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
        else:
            if str(item).count('-')==2 and str(item).count(':')==2:
                start_weekday.append(datetime.strptime(item, "%Y-%m-%d %H:%M:%S").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%Y-%m-%d %H:%M:%S")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
            elif str(item).count('-')==2 and str(item).count(':')==1:
                start_weekday.append(datetime.strptime(item, "%Y-%m-%d %H:%M").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%Y-%m-%d %H:%M")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
            elif str(item).count('-')==1 and str(item).count(':')==2:
                start_weekday.append(datetime.strptime(item, "%m-%d %H:%M:%S").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%m-%d %H:%M:%S")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
            elif str(item).count('-')==1 and str(item).count(':')==1:
                start_weekday.append(datetime.strptime(item, "%m-%d %H:%M").weekday()+1) #将日期转换为星期
                item=time.strptime(item, "%m-%d %H:%M")  #将日期字符串转换为日期格式
                start_hour.append(item.tm_hour)  #提取出时间中的小时
                start_date.append(item.tm_mday) #提取日期
                start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
    #start_year_day.append(item.tm_year,item.tm_mon,item.tm_mday)
    #print start_min[i]start_hm.append(float(start_hour[i])+float(1.0*start_min[i]/60)) 
#print start_weekday
#用day_count统计记录中出现的日期，每个日期只记录一次
    day_count=[]
    for item in start_date1:
        if(item in day_count):
            pass
        else:
            day_count.append(item)
    print "记录中出现天数：",len(day_count)  #打印出日期天数
#统计每个时间段内的通话次数:
#print min_hour,max_hour #测试用
#print cal_usetime#测试用
#检查other_phone_call中的不同电话号码数：
#print other_cell_phone
    count=0
    dic={} #字典，存放号码和对应次数
    def dic_relation():
        for item in other_cell_phone:
            if(item in dic.keys()):
                dic[item]+=1
            else:
                dic[item]=1
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
        else:
            dic_phone_day[item]=1
    for item in other_cell_phone:
            dic_phone_work[item]=1
    for item in other_cell_phone:
            dic_phone_fev[item]=1
#print dic_phone_work
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
#print dic_phone_fev   #测试
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
#input_mm()
#print dic_phone_work
#print dic_phone_fev
    for item in dic_phone_day.keys():
        if item in dic_phone_ratio.keys():
            pass
        else:
            if len(item)>=8:
                dic_phone_ratio[item]=float(1.0*(dic_phone_fev[item]-dic_phone_work[item])/(dic_phone_fev[item]+dic_phone_work[item]))
#print Min,Max #测试
#建立根据比例筛选出的号码词典：
    for interval in range(5,30):
        dic_phone_select={}
        for item in dic_phone_ratio.keys():
            if (dic_phone_ratio[item]>=-0.5 and dic_phone_ratio[item]<=1 and dic[item]>=(len(day_count)/interval)):
                dic_phone_select[item]=dic_phone_ratio[item]
        if len(dic_phone_select)<6:
            continue
        else:
            break
    print interval
    print len(dic_phone_select)
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
#print dic_phone_day
#统计每个号码打电话天数：
    phone_calldays=[] #作为记录
    for i in range(len(other_cell_phone)):
        if(other_cell_phone[i]in dic_phone_day.keys()):
            phone_calldays.append(dic_phone_day[other_cell_phone[i]])
        else:
            print 'error',other_cell_phone[i]   
        i+=1
    dic_phone_day_array=[]
#按照通话天数进行排序
    dic_phone_day_sort=sorted(dic_phone_day.iteritems(), key = lambda asd:asd[1], reverse=True)
#print dic_phone_day_sort
    for item in dic_phone_day_sort:
        dic_phone_day_array.append(item[0])   
    dic_phone_day_top10=dic_phone_day_array[0:10] #取前十
#print dic_phone_day_sort      
#print dic_phone_day
#print len(start_date)  #1173 
#print max_call_time #159
    weekday={  #转换星期
    1:'星期一',
    2:'星期二',
    3:'星期三',
    4:'星期四',
    5:'星期五',
    6:'星期六',
    7:'星期日',
    }
#rawdata1=pd.read_csv('/Users/xutao/Desktop/副本 通话详单采集1.csv') #MAC
#rawdata11=[] #写入数组中
#for i in range(len(rawdata1)):
 #   rawdata11.append(rawdata1['other_cell_phone'][i])
#print rawdata11 #测试
    final_select=[]
#print "筛选出的号码通话记录:"
    tmparray=[]
    for i in range(len(other_cell_phone)):
        if(start_hour[i]>=16 and start_hour[i]<=22  and start_weekday[i]>=5 and start_weekday[i]<=7): #and len(other_cell_phone[i])>8 )# and other_cell_phone[i][0]!='0'): #过滤掉0开始的号码):
            if(other_cell_phone[i] in dic_phone_select.keys()):  
            #print other_cell_phone[i],":通话开始时间:",start_hour[i],", 星期几通话:",weekday[start_weekday[i]],", 通话日期:",start_date1[i],"号"
                if(other_cell_phone[i] in tmparray):
                    pass
                else:
                    tmparray.append(other_cell_phone[i])
    #elif(other_cell_phone[i]=='18917009353'): #输出某个号码的通话记录
        #print other_cell_phone[i],":通话开始时间:",start_hour[i],"点, 通话时长:","s, 星期几通话:",weekday[start_weekday[i]],", 通话日期:",start_date1[i],"号,location:"
    print "筛选出的号码为:"
    if most_related_num in dic_phone_select.keys():
    #print "1 :",most_related_num
        i=0
        for item in sorted(dic_phone_select.iteritems(), key = lambda asd:asd[1], reverse=True):
            if item[0] in tmparray:
                print i+1,":",item[0]
                final_select.append(item[0])
                i+=1
            else:
                pass
    else:
        i=0
        print "1 :",most_related_num
        for item in sorted(dic_phone_select.iteritems(), key = lambda asd:asd[1], reverse=True):
            if item[0] in tmparray:
                print i+2,":",item[0]
                final_select.append(item[0])
                i+=1
            else:
                pass
    with open('/Users/xutao/Downloads/Python/data_set/phonedata_zhang/test.txt','w') as f:
        for item in final_select:
            f.write(item+'\n') #将筛选号码写入txt
