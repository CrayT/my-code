#coding:utf8
from datetime import datetime,date
import numpy as np
from dateutil.parser import parse 
from collections import Counter 
import traceback

def log(mess):
    m=datetime.now().month
    d=datetime.now().day
    n='ana_pro_'+str(m)+"-"+str(d)
    with open(str(n)+'.log','a+',encoding='utf8') as f:
        f.write(str(mess)+str(datetime.now())+'\n')
#恢复号码区号：
def phone_recover(phone_before,phone_after):
    for i in range(len(phone_before)):
        if len(str(phone_before[i]))<11: #手机号不处理
            for item in phone_after:
                if str(phone_before[i]) in str(item) and len(str(phone_before[i]))<len(str(item)):
                    phone_before[i]=item
def ini_dic(phonelist):
    dic_tmp={}
    for item in phonelist:
        dic_tmp[item]=0
    return dic_tmp
def time2se(t): #转换时间
    if str(t)=='error':
        return 0
    elif ":" not in str(t):
        return int(t)
    elif str(t).count(':')==1:
        m,s = t.strip().split(":")
        return int(m) * 60 + int(s)
    elif str(t).count(':')==2:
        h,m,s = t.strip().split(":")
        return int(h)*3600+int(m) * 60 + int(s)
    else:
        return 0
def get_gap(start_time):
    start_time2 = []
    for i in start_time:
        start_time2.append(i + ':00')
    result = sorted(start_time2, key=lambda date: datetime.strptime(date,"%Y-%m-%d %H:%M:%S"), reverse=True)
    lastday = result[0]
    firstday = result[len(result) - 1]
    year = lastday.split('-')[0]
    month = lastday.split('-')[1]
    day =  lastday.split('-')[2][0:2]
    year1 = firstday.split('-')[0]
    month1 = firstday.split('-')[1]
    day1 =  firstday.split('-')[2][0:2]
    day_cha = (datetime(int(year),int(month),int(day)) - datetime(int(year1),int(month1),int(day1))).days
    return day_cha
def get_desktop(): #获得windows桌面路径
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,\
    r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',\
    0,win32con.KEY_READ)
    return win32api.RegQueryValueEx(key,'Desktop')[0]
def function_A(start_time,phonelist,phone_list): #获取每个号码在六个月内的通话的最大间隔天数,phone_list即other_cell_phone
    phone_dic={} #号码：gap
    dic_ret={}
    try:
        for i in range(len(phonelist)):
            list_tmp=[] #M每个号码的日期列表
            for j  in range(len(start_time)):
                if phone_list[j]==phonelist[i]:
                    list_tmp.append(start_time[j])
            phone_dic[phonelist[i]]=get_gap(list_tmp)
        
        for item in phonelist:
            if phone_dic[item]<=27:
                dic_ret[item]=5.424888044
            elif phone_dic[item]>27 and phone_dic[item]<=33:
                dic_ret[item]=2.11547407
            elif phone_dic[item]>33 and phone_dic[item]<=44:
                dic_ret[item]=-0.036586964
            elif phone_dic[item]>44 and phone_dic[item]<=62:
                dic_ret[item]=-0.801349703
            elif phone_dic[item]>62 and phone_dic[item]<=110:
                dic_ret[item]=-3.61036265
            elif phone_dic[item]>110 and phone_dic[item]<=136:
                dic_ret[item]=-3.979029711
            elif phone_dic[item]>136:
                dic_ret[item]=-5.772336523
        return dic_ret
    except Exception as e:
        traceback.print_exc()   
        return 'error'
def function_B(start_date,phonelist,phone_list,dur_month):#申请日前5个月内 日通话记录 最小条数（只统计有记录天数）
    phone_dic={} #号码：num
    dic_ret={}
    try:
        if float(dur_month)<5: #通话记录不足5个月按照全部记录来计算。
            for i in range(len(phonelist)):
                list_tmp=[]
                for j in range(len(start_date)):
                    if phone_list[j]==phonelist[i]:
                        list_tmp.append(start_date[j])
                tmp=[]
                dic = Counter(list_tmp)  #统计数组中个元素个数，返回形式为字典
                for tt in dic.values():
                    tmp.append(tt)
                phone_dic[phonelist[i]]=min(tmp) #获取最小条数
        else:
            if int(max(start_date)-min(start_date))==5: #类似1 2 3 4 5 6这种，要去掉1
                tmp_date=min(start_date)+1
                for i in range(len(phonelist)):
                    list_tmp=[]
                    for j in range(len(start_date)):
                        if float(start_date[j])>=float(tmp_date):
                            if phone_list[j]==phonelist[i]:
                                list_tmp.append(start_date[j])
                    tmp=[]
                    dic = Counter(list_tmp)  #统计数组中个元素个数，返回形式为字典
                    for tt in dic.values():
                        tmp.append(tt)
                    if len(tmp)!=0: #tmp为0说明近5个月没有通话。
                        phone_dic[phonelist[i]]=min(tmp) #获取最小条数
                    else:
                        phone_dic[phonelist[i]]=0 
            else: #类似11 12 1 2 3 4 这种。要去掉11.
                tmp1=[]
                for item in start_date:
                    d=str(item).split('.')[0]
                    if len(d)==1:
                        tmp1.append(d)
                tmp_date=int(max(tmp1))+7 #例子中为单数月为4.需要去掉4+7即11月。
                for i in range(len(phonelist)):
                    list_tmp=[]
                    for j in range(len(start_date)):
                        if str(start_date[j]).split('.')[0]!=str(tmp_date): #不计算去掉的月份。
                            if phone_list[j]==phonelist[i]:
                                list_tmp.append(start_date[j])
                    tmp=[]
                    dic = Counter(list_tmp)  #统计数组中个元素个数，返回形式为字典
                    for tt in dic.values():
                        tmp.append(tt)
                    if len(tmp)!=0: #tmp为0说明近5个月没有通话。
                        phone_dic[phonelist[i]]=min(tmp) #获取最小条数
                    else:
                        phone_dic[phonelist[i]]=0 
        
        for item in phonelist:
            if phone_dic[item]<=1:
                dic_ret[item]=1.1818106913
            elif phone_dic[item]>1 and phone_dic[item]<=2:
                dic_ret[item]=-11.48609917
            elif phone_dic[item]>2:
                dic_ret[item]=-18.65522439
        return dic_ret
    except Exception as e:
        traceback.print_exc()   
        return 'error'
def function_C(start_date,phonelist,phone_list,dur_month,use_time):#申请日前5个月内通话总时长
    dic_ret={}
    phone_dic={}
    #print("use_time:",use_time)
    try:
        if float(dur_month)<5: 
            for i in range(len(phonelist)):
                tmp=0
                for j in range(len(use_time)):
                    if phone_list[j]==phonelist[i]:
                        tmp+=time2se(use_time[j])
                phone_dic[phonelist[i]]=tmp
        else:
            if int(max(start_date)-min(start_date))==5: #类似1 2 3 4 5 6这种，要去掉1
                tmp_date=min(start_date)+1
                for i in range(len(phonelist)):
                    tmp=0
                    for j in range(len(use_time)):
                        if float(start_date[j])>=float(tmp_date):
                            if phone_list[j]==phonelist[i]:
                                tmp+=time2se(use_time[j])
                    phone_dic[phonelist[i]]=tmp
            else:
                tmp1=[]
                for item in start_date:
                    d=str(item).split('.')[0]
                    if len(d)==1:
                        tmp1.append(d)
                tmp_date=int(max(tmp1))+7
                for i in range(len(phonelist)):
                    tmp=0
                    for j in range(len(use_time)):
                        if str(start_date[j]).split('.')[0]!=str(tmp_date):
                            if phone_list[j]==phonelist[i]:
                                tmp+=time2se(use_time[j])
                    phone_dic[phonelist[i]]=tmp
        #print("phone_dic:",phone_dic)
        for item in phonelist:
            if int(phone_dic[item])<=238:
                dic_ret[item]=-10.5303
            elif int(phone_dic[item])>238 and int(phone_dic[item])<=342:
                dic_ret[item]=-9.588832248
            elif int(phone_dic[item])>342 and int(phone_dic[item])<=521:
                dic_ret[item]=-7.804042147
            elif int(phone_dic[item])>521 and int(phone_dic[item])<=942:
                dic_ret[item]=-5.164131972
            elif int(phone_dic[item])>942 and int(phone_dic[item])<=1294:
                dic_ret[item]=-1.113717626
            elif int(phone_dic[item])>1294 and int(phone_dic[item])<=1529:
                dic_ret[item]=2.8652344528
            elif int(phone_dic[item])>1529 and int(phone_dic[item])<=2720:
                dic_ret[item]=3.1871679739
            elif int(phone_dic[item])>2720 and int(phone_dic[item])<=6285:
                dic_ret[item]=5.638299171
            elif int(phone_dic[item])>6285 and int(phone_dic[item])<=8581:
                dic_ret[item]=7.5679954566
            elif int(phone_dic[item])>8581 and int(phone_dic[item])<=11998:
                dic_ret[item]=8.3371979762
            else:
                dic_ret[item]=13.26397752
        return dic_ret
    except Exception as e:
        traceback.print_exc() 
        return 'error'
def function_D(start_weekend,start_date,phonelist,phone_list,dur_month,use_time):#申请日前2个月内休息日通话时长的最小值
    phone_dic={} 
    dic_ret={}
    try:
        if float(dur_month)<2:
            for i in range(len(phonelist)):
                list_tmp=[]
                for j in range(len(use_time)):
                    if start_weekend[j]>=6 and  start_weekend[j]<=7: #休息日
                        if phone_list[j]==phonelist[i]:
                            list_tmp.append(time2se(use_time[j]))
                if len(list_tmp)!=0:
                    phone_dic[phonelist[i]]=min(list_tmp)
                else:
                    phone_dic[phonelist[i]]=0
        else:
            if int(max(start_date)-min(start_date))<6: 
                tmp_date=max(start_date)-2
                for i in range(len(phonelist)):
                    list_tmp=[]
                    for j in range(len(use_time)):
                        if float(start_date[j])>=float(tmp_date): #过滤去掉月份
                            if start_weekend[j]>=6 and start_weekend[j]<=7: #休息日
                                if phone_list[j]==phonelist[i]:
                                    list_tmp.append(time2se(use_time[j]))
                    if len(list_tmp)!=0:
                        phone_dic[phonelist[i]]=min(list_tmp)
                    else:
                        phone_dic[phonelist[i]]=0
            else:
                tmp1=[]
                for item in start_date:
                    d=str(item).split('.')[0]
                    if len(d)==1 and (d not in tmp1) and int(d) <7:
                        tmp1.append(d)
                for i in range(len(phonelist)):
                    list_tmp=[]
                    for j in range(len(start_date)):
                        if len(tmp1)==1:#只保留12 1月
                            if str(start_date[j]).split('.')[0]=='1'  or str(start_date[j]).split('.')[0]=='12': #不计算去掉的月份。
                                if phone_list[j]==phonelist[i]:
                                    if start_weekend[j]>=6 and start_weekend[j]<=7: #工作日
                                        list_tmp.append(time2se(use_time[j]))
                        elif len(tmp1)==2: #1 2
                            if str(start_date[j]).split('.')[0]=='1' or str(start_date[j]).split('.')[0]=='2': #不计算去掉的月份。
                                if phone_list[j]==phonelist[i]:
                                    if start_weekend[j]>=6 and start_weekend[j]<=7: #休息日
                                        list_tmp.append(time2se(use_time[j]))
                        else: #12 1 2 3 4 5这类，只要与5的差的绝对值在2以内，就是2个月内。
                            if abs(int(str(start_date[j]).split('.')[0]) - int(max(tmp1)))<2:
                                if phone_list[j]==phonelist[i]:
                                    if start_weekend[j]>=6 and start_weekend[j]<=7: #工作日
                                        list_tmp.append(time2se(use_time[j]))
                    if len(list_tmp)!=0:
                        phone_dic[phonelist[i]]=min(list_tmp)
                    else:
                        phone_dic[phonelist[i]]=0
        for item in phonelist:
            if int(phone_dic[item])<=37:
                dic_ret[item]=5.9927480344
            elif int(phone_dic[item])>37 and int(phone_dic[item])<=63:
                dic_ret[item]=3.691018281
            elif int(phone_dic[item])>63 and int(phone_dic[item])<=387:
                dic_ret[item]=1.0544188718
            elif int(phone_dic[item])>387:
                dic_ret[item]=-8.568019606
        return dic_ret
    except Exception as e:
        traceback.print_exc()   
        return 'error'
def function_E(start_date,start_hour,phonelist,phone_list,dur_month):#申请日前5个月内在6点到11点之间 呼入记录 数占所有通话记录数的比例（不区分呼入呼出） 
    phone_dic1={}
    phone_dic={}
    dic_ret={}
    try:
        for i in range(len(phonelist)): #初始化
            phone_dic1[phonelist[i]]=0
        if float(dur_month)<5: #通话记录不足5个月
            for i in range(len(phone_list)):
                if int(start_hour[i])>=6 and int(start_hour[i])<11:
                    phone_dic1[phone_list[i]]=int(phone_dic1[phone_list[i]])+1
            leng=len(phone_list)
            for i in range(len(phonelist)):
                phone_dic[phonelist[i]]='%.4f'%(phone_dic1[phonelist[i]]/leng)
        else:
            if int(max(start_date)-min(start_date))==5: #类似1 2 3 4 5 6这种，要去掉1
                tmp_date=min(start_date)+1
                for i in range(len(phone_list)):
                    if float(start_date[i])>=float(tmp_date):
                        if int(start_hour[i])>=6 and int(start_hour[i])<11:
                            phone_dic1[phone_list[i]]=int(phone_dic1[phone_list[i]])+1
                leng=len(phone_list)
                for i in range(len(phonelist)):
                    phone_dic[phonelist[i]]='%.4f'%(phone_dic1[phonelist[i]]/leng)
            else:
                tmp1=[]
                for item in start_date:
                    d=str(item).split('.')[0]
                    if len(d)==1:
                        tmp1.append(d)
                tmp_date=int(max(tmp1))+7 #例子中为单数月为4.需要去掉4+7即11月。
                for i in range(len(phone_list)):
                    if str(start_date[i]).split('.')[0]!=str(tmp_date): #不计算去掉的月份。
                        if int(start_hour[i])>=6 and int(start_hour[i])<11:
                            phone_dic1[phone_list[i]]=int(phone_dic1[phone_list[i]])+1
                leng=len(phone_list)
                for i in range(len(phonelist)):
                    phone_dic[phonelist[i]]='%.4f'%(phone_dic1[phonelist[i]]/leng)
        for item in phonelist:
            if float(phone_dic[item])<=0.0262:
                dic_ret[item]=6.575846258
            elif float(phone_dic[item])>0.0262 and float(phone_dic[item])<= 0.1244 :
                dic_ret[item]=3.4150940198
            elif float(phone_dic[item])>0.1244 and float(phone_dic[item])<= 0.166 :
                dic_ret[item]=1.7550101573
            elif float(phone_dic[item])> 0.166  and float(phone_dic[item])<= 0.1995 :
                dic_ret[item]=0.4110557047
            elif float(phone_dic[item])> 0.1995  and float(phone_dic[item])<=0.325:
                dic_ret[item]=-1.560838162
            elif float(phone_dic[item])>0.325:
                dic_ret[item]=-5.056723647
        return dic_ret
        
    except Exception as e:
        traceback.print_exc()
        return 'error'
def function_F(init_type,start_hour,phonelist,phone_list):#申请日前6个月内在21点到01点之间 呼出记录 数占所有通话记录数的比例
    phone_dic={}
    phone_dic1={}
    dic_ret={}
    try:
        for i in range(len(phonelist)): #初始化
            phone_dic1[phonelist[i]]=0
        for i in range(len(phone_list)):
            if int(start_hour[i])>=21 or int(start_hour[i])<=1:
                if init_type[i]=='主叫':
                    phone_dic1[phone_list[i]]=int(phone_dic1[phone_list[i]])+1
        leng=len(phone_list)
        for i in range(len(phonelist)):
            phone_dic[phonelist[i]]='%.4f'%(phone_dic1[phonelist[i]]/leng)
        
        for item in phonelist:
            if float(phone_dic[item])<=0.016:
                dic_ret[item]=8.4820253906
            elif float(phone_dic[item])>0.016 and float(phone_dic[item])<=0.0383 :
                dic_ret[item]=7.4622653527
            elif float(phone_dic[item])>0.0383  and float(phone_dic[item])<=0.0513 :
                dic_ret[item]=7.036194014
            elif float(phone_dic[item])>0.0513  and float(phone_dic[item])<=0.2305 :
                dic_ret[item]=5.9889821926
            elif float(phone_dic[item])>0.2305 :
                dic_ret[item]=-5.655053362
        return dic_ret
    except Exception as e:
        traceback.print_exc()
        return 'error'
def function_G(init_type,start_date,phonelist,phone_list):#申请日前6个月内最近一次呼出距离申请日天数
    phone_dic={}
    phone_dic1={}
    dic_ret={}
    list_tmp0=[]
    try:
        for item in start_date:
            list_tmp0.append(str(item) + ':00')
        tmp_date=sorted(list_tmp0, key=lambda date: datetime.strptime(date,"%Y-%m-%d %H:%M:%S"), reverse=True)[0]
        for i in range(len(phonelist)):
            list_tmp=[]
            for j in range(len(start_date)):
                if phonelist[i]==phone_list[j]:
                    if str(init_type[j])=='主叫': #可能有些号码没有主叫，那么list_tmp数组会为空。
                        list_tmp.append(start_date[j])

            start_time2 = []
            if len(list_tmp)!=0:
                for item in list_tmp:
                    start_time2.append(str(item) + ':00')
            else: #list_tmp为空是，给这个号码通话记录中的最近日期，让他的最后的得分为0！
                start_time2.append("2010-01-01 00:00:00")
            list_tmp2 = sorted(start_time2, key=lambda date: datetime.strptime(date,"%Y-%m-%d %H:%M:%S"), reverse=True)[0]
            date_most_near=list_tmp2 #最后一个日期
            a1 = parse(tmp_date)   #datetime 模块处理时间
            a2 = parse(date_most_near)  
            day_gap=(a1-a2).days  
            if day_gap>1000:
                phone_dic[phonelist[i]]=0.1
            else:
                phone_dic[phonelist[i]]=day_gap

        for item in phonelist:
            if phone_dic[item]==0.1:
                dic_ret[item]=0
            elif phone_dic[item]<=2:
                dic_ret[item]=10.184982602
            elif phone_dic[item]>2 and phone_dic[item]<=4:
                dic_ret[item]=8.1155618579
            elif phone_dic[item]>4 and phone_dic[item]<=5:
                dic_ret[item]=6.9613270106
            elif phone_dic[item]>5 and phone_dic[item]<=6:
                dic_ret[item]=4.5959367779
            elif phone_dic[item]>6 and phone_dic[item]<=16:
                dic_ret[item]=2.6226433698
            elif phone_dic[item]>16 and phone_dic[item]<=34:
                dic_ret[item]=1.1170475316
            elif phone_dic[item]>34 and phone_dic[item]<=44:
                dic_ret[item]=-1.384859674
            elif phone_dic[item]>44 and phone_dic[item]<=66:
                dic_ret[item]=-4.010604391
            elif phone_dic[item]>66 and phone_dic[item]<=90:
                dic_ret[item]=-5.424703276
            elif phone_dic[item]>90:
                dic_ret[item]=-9.074354137
        return dic_ret
    except Exception as e:
        traceback.print_exc()
        return 'error'
def function_H(init_type,start_weekend,start_date,phonelist,phone_list,dur_month):#申请日前3个月内 工作日 日呼出 最小条数（只统计有记录天数）
    phone_dic={} #号码：num
    dic_ret={}
    try:
        if float(dur_month)<3: #通话记录不足3个月按照全部记录来计算。
            for i in range(len(phonelist)):
                list_tmp=[]
                for j in range(len(start_date)):
                    if start_weekend[j]>=1 and  start_weekend[j]<=5: #工作日
                        if phone_list[j]==phonelist[i]:
                            if init_type[j]=='主叫':
                                list_tmp.append(start_date[j])
                tmp=[]
                dic = Counter(list_tmp)  #统计数组中个元素个数，返回形式为字典
                for tt in dic.values():
                    tmp.append(tt)
                if len(tmp)!=0: #tmp为0说明近5个月没有通话。
                        phone_dic[phonelist[i]]=min(tmp) #获取最小条数
                else:
                    phone_dic[phonelist[i]]=0 
        else:
            if int(max(start_date)-min(start_date))<6: #类似1 2 3 4 5 6这种，要去掉1 2 3
                tmp_date=max(start_date)-3
                for i in range(len(phonelist)):
                    list_tmp=[]
                    for j in range(len(start_date)):
                        if phone_list[j]==phonelist[i]:
                            if float(start_date[j])>=float(tmp_date): #过滤去掉月份
                                if start_weekend[j]>=1 and start_weekend[j]<=5: #工作日
                                    if init_type[j]=='主叫':
                                        list_tmp.append(start_date[j])
                    tmp=[]
                    dic = Counter(list_tmp)  #统计数组中个元素个数，返回形式为字典
                    for tt in dic.values():
                        tmp.append(tt)
                    if len(tmp)!=0: #tmp为0说明近5个月没有通话。
                        phone_dic[phonelist[i]]=min(tmp) #获取最小条数
                    else:
                        phone_dic[phonelist[i]]=0 
            else: #类似11 12 1 2 3 4 这种。要去掉11.
                tmp1=[]
                for item in start_date:
                    d=str(item).split('.')[0]
                    if len(d)==1 and (d not in tmp1) and int(d) <7:
                        tmp1.append(d)
                for i in range(len(phonelist)):
                    list_tmp=[]
                    for j in range(len(start_date)):
                        if len(tmp1)==1:#只保留11 12 1月
                            if phone_list[j]==phonelist[i]:
                                if str(start_date[j]).split('.')[0]=='1' or str(start_date[j]).split('.')[0]=='11' or str(start_date[j]).split('.')[0]=='12': #不计算去掉的月份。
                                    if init_type[j]=='主叫':
                                        list_tmp.append(start_date[j])
                        elif len(tmp1)==2:#只保留12 1 2月
                            if phone_list[j]==phonelist[i]:
                                if str(start_date[j]).split('.')[0]=='1' or str(start_date[j]).split('.')[0]=='2' or str(start_date[j]).split('.')[0]=='12': #不计算去掉的月份。
                                    if init_type[j]=='主叫':
                                        list_tmp.append(start_date[j])
                        elif len(tmp1)==3: #1 2 3。
                            if phone_list[j]==phonelist[i]:
                                if str(start_date[j]).split('.')[0] in tmp1:
                                    if init_type[j]=='主叫':
                                        list_tmp.append(start_date[j])
                        else: #12 1 2 3 4 5这类，只要与5的差的绝对值在3以内，就是3个月内。
                            if phone_list[j]==phonelist[i]:
                                if abs(int(str(start_date[j]).split('.')[0]) - int(max(tmp1)))<3:
                                    if init_type[j]=='主叫':
                                        list_tmp.append(start_date[j])
                    tmp=[]
                    dic = Counter(list_tmp)  #统计数组中个元素个数，返回形式为字典
                    for tt in dic.values():
                        tmp.append(tt)
                    if len(tmp)!=0: #tmp为0说明近5个月没有通话。
                        phone_dic[phonelist[i]]=min(tmp) #获取最小条数
                    else:
                        phone_dic[phonelist[i]]=0 
        
        for item in phonelist:
            if phone_dic[item]<=1:
                dic_ret[item]=3.2530185824
            elif phone_dic[item]>1:
                dic_ret[item]=-9.377878727
        return dic_ret
    except Exception as e:
        traceback.print_exc()   
        return 'error'