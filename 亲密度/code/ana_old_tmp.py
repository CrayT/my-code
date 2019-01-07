#--coding:utf-8--
import sys
import os
import time
import datetime
from datetime import datetime,date
from phone_info_v3 import read_file
import traceback
from function import get_gap

def select(address,num_get):
    num_Get=num_get
    try:
        if num_Get:
            num_get=int(num_Get) #若有定义输入，则用定义，否则默认为5个
    except:
        num_get=5
    start_hour=[]  #存放日期中的小时
    start_date=[]  #存放日-day
    start_date1=[] #存放月日,比如10月2号，以10.02数字存放
    start_weekday=[] #存放星期几
    phonelist=[] #存放号码，每个号码唯一；
    bj=0 #被叫数量 ，后面代买已注释。
    zj=0 #主叫数量
    year=datetime.now().year  #获取当前年份
    month=datetime.now().month #获取当前月份
    for item in start_time:
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
            if int(item[0:2])<=int(month):
                item=str(year)+"-"+str(item) #如果日期当中缺少年份，若月份小于当前实际月份，则添加当前年份，否则添加去年年份
            else:
                item=str(int(year)-1)+"-"+str(item)
            start_weekday.append(datetime.strptime(item, "%Y-%m-%d %H:%M:%S").weekday()+1) #将日期转换为星期
            item=time.strptime(item, "%Y-%m-%d %H:%M:%S")  #将日期字符串转换为日期格式
            start_hour.append(item.tm_hour)  #提取出时间中的小时
            start_date.append(item.tm_mday) #提取日期
            start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
        elif str(item).count('-')==1 and str(item).count(':')==1:
            if int(item[0:2])<=int(month):
                item=str(year)+"-"+str(item) #如果日期当中缺少年份，若月份小于当前实际月份，则添加当前年份，否则添加去年年份
            else:
                item=str(int(year)-1)+"-"+str(item)
            start_weekday.append(datetime.strptime(item, "%Y-%m-%d %H:%M").weekday()+1) #将日期转换为星期
            item=time.strptime(item, "%Y-%m-%d %H:%M")  #将日期字符串转换为日期格式
            start_hour.append(item.tm_hour)  #提取出时间中的小时
            start_date.append(item.tm_mday) #提取日期
            start_date1.append(float(item.tm_mon)+float(1.0*(item.tm_mday)/100))
        else:
            string=str(address)+"time数据格式有误，请参照File-help！"
            dial=MessageDialog(None,string)
            dial.ShowModal()
            exit()

    for item in other_cell_phone:#添加进每个文件的号码
        if item in phonelist:
            pass
        else:
            phonelist.append(item)
    #用day_count统计记录中出现的日期，每个日期只记录一次
    day_count=[]
    for item in start_date1:
        if(item in day_count):
            pass
        else:
            day_count.append(item)

    dic={} #存放 号码:通话次数
    for item in other_cell_phone:
        if(item in dic.keys()):
            dic[item]+=1
        else:
            dic[item]=1
    #一个号码若每天都打电话，则标记为1
    dic_phone_day={}
    dic_phone_work={}#统计工作日天数
    dic_phone_fev={}#节假日
    #先全部置一。
    for item in other_cell_phone:
        dic_phone_work[item]=1
        dic_phone_fev[item]=1
        dic_phone_day[item]=1 
    #统计每个号码的工作日和周六周末通话数
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
            i+=1
        dic_phone_work[item]=j
        dic_phone_fev[item]=f
    dic_phone_ratio={} #存放通话通话比例
    for item in dic_phone_day.keys(): #item为号码
        if item in dic_phone_ratio.keys():
            pass
        else:
            if len(item)>=8:
                dic_phone_ratio[item]=float(1.0*(dic_phone_fev[item]-dic_phone_work[item])/(dic_phone_fev[item]+dic_phone_work[item]))
    #根据阈值筛选出号码：
    dic_phone_select1={}
    for day_Gap in range(10,35,5): #为保证找出指定个数的号码，这里调整通话天数，先要求平均至少10天通话一次，15天次之，然后最差35天一次
        for item in dic_phone_ratio.keys():
            if dic[item]>=(len(day_count)/day_Gap):
                dic_phone_select1[item]=dic_phone_ratio[item]
        if len(dic_phone_select1)>num_get:
            break
    #然后根据阈值排序从大到小筛选出号码：  
    dic_phone_select={}
    i=0
    for item in sorted(dic_phone_select1.items(), key = lambda asd:asd[1], reverse=True) :
        if i<num_get: #取前num_get个
            dic_phone_select[item[0]]=dic_phone_ratio[item[0]]  #按照从大到小排序输出,python2.7中sorted之后出来的item是元祖格式，提取号码需要item[0],python3不是这样。
            i+=1
        else:
            break
    #如下代码作用：统计出所有号码通话天数，即若某天有通话(无论一天中通话多少次)，则加一，
    for item in dic_phone_day.keys():
        j=0
        tmp=[]
        for call in other_cell_phone:
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
    most_related_num=max(dic_phone_day.items(),key=lambda x:x[1])[0] #最长通话天数号码
    tmparray=[]
    for i in range(len(other_cell_phone)):
        if(start_hour[i]>=16   and start_weekday[i]>=5 and start_weekday[i]<=7 and len(other_cell_phone[i])>=8):# and other_cell_phone[i][0]!='0'): #过滤掉0开始的号码):
            if(other_cell_phone[i] in dic_phone_select.keys()):  
                if(other_cell_phone[i] in tmparray):
                    pass
                else:
                    tmparray.append(other_cell_phone[i])
    if most_related_num in dic_phone_select:
        i=0
        for item in sorted(dic_phone_select, key = lambda asd:asd[1], reverse=True):
            if i>=num_get:
                break
            elif item in tmparray:
                final_select_tmp.append(item)
                i+=1
    else:
        i=0
        final_select_tmp.append(most_related_num)
        final_select_counts.append(dic[most_related_num])
        for item in sorted(dic_phone_select, key = lambda asd:asd[1], reverse=True):
            if i>num_get:
                break
            elif item in tmparray:
                final_select_tmp.append(item)
                i+=1

    for item in final_select_tmp:
        final_select_tmp_ratio.append(dic_phone_ratio[item])
        final_select_tmp_num.append(dic[item])

    phone_recover(final_select_tmp,phone_with_id) #恢复区号；

#根据address的文件名，调用对应解析函数
def get_function_old(path,num_get):
    global other_cell_phone#定义全局数组，这样每次调用一个文件，都会产生新数组，防止不同文件相互叠加
    global phone_with_id #带区号
    global start_time #通话日期
    global final_select_tmp #返回的号码数组
    global final_select_tmp_ratio #返回的号码ratio数组
    global final_select_tmp_num #返回的号码通话次数数组
    final_select_tmp=[]
    final_select_tmp_ratio=[]
    final_select_tmp_num=[]
    phone_with_id=[]
    other_cell_phone=[]
    start_time=[]
    try:
        result=read_file(path)
        if len(result['calls'])==0 or result['calls']=='error':
            return "None"
        else:
            for it in result['calls']:
                start_time.append(it['st'])
                other_cell_phone.append(it['phone'][1])
                phone_with_id.append(it['phone'][0])
            select(path,num_get)
            return final_select_tmp,final_select_tmp_ratio,final_select_tmp_num #返回号码，阈值，通话次数
    except:
        traceback.print_exc()
        return "error"