#coding:utf8
import win_unicode_console #防止因print出现OS错误
win_unicode_console.enable()
import json
import re

def crime_form(address):
    with open(address,encoding='utf8') as f: #20180305102605798
    #with open('E:\\魏老师\\受案登记表\\7.txt',encoding='utf8') as f:
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n') #java转出来的txt开头有\ufeff，python直接读取报错。
            a.append(line)
    with open("config.json",'r',encoding='utf8') as f: #ubuntu
            config = json.load(f)
    dic_ret={}

    list_1=[]
    list_2=[]
    list_3=[]
    list1=sorted(config["民警"].items(), key = lambda asd:asd[1], reverse=True)
    list2=sorted(config["时间"].items(), key = lambda asd:asd[1], reverse=True)
    list3=sorted(config["地点"].items(), key = lambda asd:asd[1], reverse=True)
    for i in range(len(list1)):
        list_1.append(list1[i][1])
    for i in range(len(list2)):
        list_2.append(list2[i][1])
    for i in range(len(list3)):
        list_3.append(list3[i][1])

    pattern = re.compile(r'\d+')    #用于匹配接报时间的日期开始位置 
    pattern2=re.compile(u"[\u4E00-\u9FA5]") #匹配汉字

    for item in list_1:
        for i in range(len(a)):
            if item in a[i]:
                if len(a[i])<=5:
                    #print(item,a[i+1])
                    dic_ret[item]=a[i+1]
                    break_flag1=True
                    break
                else:
                    m=pattern2.search(str(a[i][4:])) #从第四个位置开始匹配汉字，默认为地址的开始位置
                    index=m.start(0)
                    #print(item,a[i][len(item):][index:])
                    dic_ret[item]=a[i][len(item):][index:]
                    break_flag1=True
                    break
            else:
                break_flag1=False
        if break_flag1==True:
            break
    if not break_flag1:
        dic_ret["接报民警"]="None"

    pattern3 = re.compile(r"(\d{4}.\d{1,2}.\d{1,2})")#定义匹配模式
    for item in list_2:
        for i in range(len(a)):
            if item in a[i]:
                if len(a[i])<=5:
                    #print(item,a[i+1])
                    dic_ret[item]=a[i+1]
                    break_flag2=True
                    break
                else:
                    m=pattern3.search(str(a[i])) #按照正则表达式匹配日期，不再按照数字，格式为1111*11*11
                    if not m: #在当前行没有匹配到日期，匹配下一行
                        st=re.findall(pattern3,a[i+1])
                        #print(item,st[0])
                        dic_ret[item]=st[0]
                        break_flag2=True
                        break
                    else:
                        st=re.findall(pattern3,a[i])
                        #print(item,st[0])
                        dic_ret[item]=st[0]
                        break_flag2=True
                        break
            else:
                break_flag2=False
        if break_flag2==True:
            break
    if not break_flag2:
        dic_ret["接报时间"]="None"

    for item in list_3:
        for i in range(len(a)):
            if item in a[i]:
                t=i
                if len(a[i])<=5:
                    #print(item,a[i+1])
                    dic_ret[item]=a[i+1]
                    break_flag3=True
                    break
                else:
                    if a[i].endswith(item): #当前行的地点在字符串的最后，说明真实地点在下一行
                        dic_ret[item]=a[i+1]
                        break_flag3=True
                        #print(item,a[i+1])
                        break
                    else:
                        m=pattern2.search(str(a[i][len(item):])) #在当前行匹配地址，从第四个位置开始匹配汉字，默认为地址的开始位置
                        index=m.start(0)
                        #print(item,a[i][len(item):][index:])
                        dic_ret[item]=a[i][len(item):][index:]
                        break_flag3=True
                        break
            else:
                break_flag3=False
        if break_flag3==True:
            break
    if not break_flag3:
        dic_ret["接报地点"]="None"

    for i in range(t,len(a)):
        if str(a[i])[:4].isdigit():
            index_start=i
            break
    for i in range(t,len(a)):
        if '建议' in a[i]:
            index_end=i
    s=''
    for i in range(index_start,index_end):
        s=s+str(a[i])

    dic_ret['案情经过']=s
    
    return dic_ret
