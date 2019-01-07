#coding:utf8
import re
import json
def chuan_huan_form(address):
    with open(address,encoding='utf8') as f: #20180305102605798
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n') #java转出来的txt开头有\ufeff，python直接读取报错。
            a.append(line)
    with open("config.json",'r',encoding='utf8') as f: #ubuntu
            config = json.load(f)
    dic_config=config['chuan_huan'] #读取配置文件的关键字
    dic_ret={}
    flag_1=False
    flag_2=False
    for i in range(len(a)):
        if not flag_1:
            if "根据" in a[i]:
                index_start=i
                flag_1=True
        if not flag_2:
            if "接受传唤" in a[i] or "依法拘传" in a[i] :
                index_end=i
                flag_2=True
    s=''
    for i in range(index_start,index_end+1):
        s+=a[i]
    pattern = re.compile(r"(\d{4})")
    dic1=dic_config['罪名']
    item1=dic1['1'] #读取关键字
    item2=dic1['2']
    if item1 in s and item2 in s:
        t1=s.index(item1)
        t2=s.index(item2)
        dic_ret["罪名"]=s[t1+2:t2]
    else:
        dic_ret["罪名"]=None
    dic2=dic_config['嫌疑人']
    item1=dic2['1'] #读取关键字
    item2=dic2['2']
    if item1 in s and '(' in s:
        t3=s.index('嫌疑人')
        t4=s.index('(')
        dic_ret["嫌疑人"]=s[t3+3:t4]
    elif  item1 in s and item2 in s: #防止'('没有识别出来的情况。
        t3=s.index(item1)
        t4=s.index(item2)
        dic_ret["嫌疑人"]=s[t3+3:t4]
    else:
        dic_ret["嫌疑人"]=None
    pattern2=re.compile(u"[\u4E00-\u9FA5]") #匹配汉字
    if '性别' in s:
        t5=s.index('性别')
        m=pattern2.search(str(s[t5+2:])) #匹配'性别'后面的第一个汉字为性别，防止出现'_'等符号。
        index=m.start(0)
        dic_ret["性别"]=s[t5+index:][2]
    else:
        dic_ret["性别"]=None
    dic2=dic_config['出生日期']
    item1=dic2['1'] #读取关键字
    item2=dic2['2']
    if item1 in s and item2 in s:
        t6=s.index(item1)
        t7=s.index(item2)
        dic_ret["出生日期"]=s[t6+4:t7-1].strip("_")
    else:
        dic_ret["出生日期"]=None
    dic2=dic_config['住址']
    item1=dic2['1'] #读取关键字
    item2=dic2['2'] 
    if item1 in s or item2 in s: #以')' 和关键字'于'定位地址最后位置。
        if item1 in s:
            t8=s.index(item1)
        if item2 in s:
            t8=s.index(item2)
        dic_ret["住址"]=s[t7+2:t8-1]
    elif re.findall(pattern,s[t7:]): #如果没有')' 和关键字'于'，则匹配后面的日期作为地址的紧跟字符。
        t9=s[t7:].index(re.findall(pattern,s[t7:])[0])
        dic_ret["住址"]=s[t7+2:t7+t9]
    else:
        dic_ret["住址"]=None
    return dic_ret