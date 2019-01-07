#--coding:utf-8--
import sys
import os
import pandas as pd
import numpy as np
import time
import datetime
from datetime import datetime,date
from wx import *
from function import *
from phone_info_v3 import read_file
import traceback
def select(address,num_get):
    log("start to select...")
    num_Get=num_get
    try:
        if num_Get:
            num_get=int(num_Get) #若有定义输入，则用定义，否则默认为5个
    except:
        num_get=5
    phonelist=[]

    start_hour=[]  #存放日期中的小时
    start_date=[]  #存放日-day
    start_date1=[] #存放月日,比如10月2号，以10.02数字存放
    start_weekday=[] #存放星期几
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
    
    dur_date=get_gap(start_time) #获取通话记录的第一天和最后一天间隔天数。
    dur_month='%.1f'%(dur_date/30)

    try:
        dic_A=function_A(start_time,phonelist,other_cell_phone)
        if dic_A=='error':
            dic_A=ini_dic(phonelist)
    except Exception as e:
        log("function_A")
        log(e)

    try:
        dic_B=function_B(start_date1,phonelist,other_cell_phone,dur_month)
        if dic_B=='error':
            dic_B=ini_dic(phonelist)
    except Exception as e:
        log("function_C")
        log(e)

    try:
        dic_C=function_C(start_date1,phonelist,other_cell_phone,dur_month,use_time)
        if dic_C=='error':
            dic_C=ini_dic(phonelist)
    except Exception as e:
        log("function_C")
        log(e)

    try:
        dic_D=function_D(start_weekday,start_date1,phonelist,other_cell_phone,dur_month,use_time)
        if dic_D=='error':
            dic_D=ini_dic(phonelist)
    except Exception as e:
        log("function_D")
        log(e)

    try:
        dic_E=function_E(start_date1,start_hour,phonelist,other_cell_phone,dur_month)
        if dic_E=='error':
            dic_E=ini_dic(phonelist)
    except Exception as e:
        log("function_E")
        log(e)

    try:
        dic_F=function_F(init_type,start_hour,phonelist,other_cell_phone)
        if dic_F=='error':
            dic_F=ini_dic(phonelist)
    except Exception as e:
        log("function_F")
        log(e)

    try:
        dic_G=function_G(init_type,start_time,phonelist,other_cell_phone)
        if dic_G=='error':
            dic_G=ini_dic(phonelist)
    except Exception as e:
        log("function_G")
        log(e)

    try:
        dic_H=function_H(init_type,start_weekday,start_date1,phonelist,other_cell_phone,dur_month)
        if dic_H=='error':
            dic_H=ini_dic(phonelist)
    except Exception as e:
        log("function_H")
        log(e)

    dic_ratio_tmp={}
    for item in phonelist:
        dic_ratio_tmp[item]=float(dic_A[item])+float(dic_B[item])+float(dic_C[item])+float(dic_D[item])+float(dic_E[item])+float(dic_F[item])+float(dic_G[item])+float(dic_H[item])

    i=1
    for item in sorted(dic_ratio_tmp.items(), key = lambda asd:asd[1], reverse=True):
        if (len(item[0])<=9 and str(item[0]).startswith('0')) or str(item[0]).startswith('9') or len(str(item[0]))<=3 or (len(item[0])<=9 and str(item[0]).startswith('1')): #去除服务号码
            pass
        else:
            final_select_tmp.append(item[0])
            i+=1
            if i>num_get:
                break

    for item in final_select_tmp:
        final_select.append(item)
        final_select_dicA.append(dic_A[item])
        final_select_dicB.append(dic_B[item])
        final_select_dicC.append(dic_C[item])
        final_select_dicD.append(dic_D[item])
        final_select_dicE.append(dic_E[item])
        final_select_dicF.append(dic_F[item])
        final_select_dicG.append(dic_G[item])
        final_select_dicH.append(dic_H[item])

    phone_recover(final_select_tmp,phone_with_id)

#根据address的文件名，调用对应解析函数
def get_function_new(path,num_get):
    global phone_with_id
    global other_cell_phone#定义全局数组
    global start_time
    global final_select_tmp
    global final_select_dicA
    global final_select_dicB
    global final_select_dicC
    global final_select_dicD
    global final_select_dicE
    global final_select_dicF
    global final_select_dicG
    global final_select_dicH
    global init_type
    global use_time

    log("get_function start..")
    log(str(path))

    use_time=[]
    init_type=[]
    final_select_tmp=[]
    final_select_dicA=[]
    final_select_dicB=[]
    final_select_dicC=[]
    final_select_dicD=[]
    final_select_dicE=[]
    final_select_dicF=[]
    final_select_dicG=[]
    final_select_dicH=[]
    other_cell_phone=[]
    start_time=[]
    phone_with_id=[]
    try:
        result=read_file(path)
        if len(result['calls'])==0 or result['calls']=='error':
            log("获取calls 失败...")
            return "None"
        else:
            log("获取calls成功...")
            for it in result['calls']:
                start_time.append(it['st']) #start_time
                init_type.append(it['it']) #主被叫
                use_time.append(it['ut']) #通话时长
                other_cell_phone.append(it['phone'][1])
                phone_with_id.append(it['phone'][0])
            select(path,num_get)
            return final_select_tmp,final_select_dicA,final_select_dicB,final_select_dicC,final_select_dicD,final_select_dicE,final_select_dicF,final_select_dicG,final_select_dicH
    except Exception as e:
        log(str(e))
        traceback.print_exc()
        return "error"