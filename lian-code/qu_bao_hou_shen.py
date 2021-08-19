#coding:utf8
import re
import json
def qu_bao_form(address):
    with open(address,encoding='utf8') as f: #20180305102605798
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n') #java转出来的txt开头有\ufeff，python直接读取报错。
            a.append(line)
    with open("config.json",'r',encoding='utf8') as f: #ubuntu
            config = json.load(f)
    dic_config=config['qu_bao'] #读取配置文件的关键字
    dic_ret={}
    flag_1=False
    flag_2=False
    for i in range(len(a)):
        if not flag_1: #加标志位，一旦识别出关键字就不在试探，防止出现下文也有该关键字
            if "犯罪嫌疑" in a[i]:
                index_start=i
                flag_1=True
        if not flag_2:
            if "我局" in a[i]:
                index_end=i
                flag_2=True
    s=''
    for i in range(index_start,index_end+1):
        s+=a[i]
    pattern=re.compile(u"[\u4E00-\u9FA5]") #匹配汉字
    dic1=dic_config['姓名']
    item1=dic1['1'] #读取关键字
    item2=dic1['2']
    if item1 in s and item2 in s: #以关键字嫌疑人和性别匹配姓名，防止汉字之间没有分隔符
        t1=s.index(item1)
        t2=s.index(item2)
        name=s[t1+3:t2].strip(',_ ') #
        dic_ret["姓名"]=name
    else:
        dic_ret["姓名"]=None
    if '性别' in s:
        t3=s.index('性别')
        m=pattern.search(str(s[t3+2:])) #匹配'性别'后面的第一个汉字为性别，防止出现'_'等符号。
        index=m.start(0)
        dic_ret["性别"]=s[t3+index:][2]
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
    dic3=dic_config['住址']
    item1=dic3['1'] #读取关键字
    item2=dic3['2']
    if item1 in s and item2 in s:
        t8=s.index(item1)
        t9=s.index(item2)
        dic_ret["住址"]=s[t8+2:t9].strip("_,")
    else:
        dic_ret["住址"]=None
    dic4=dic_config['职业']
    item1=dic4['1'] #读取关键字
    item2=dic4['2']
    if item1 in s and item2 in s:
        t10=s.index(item1)
        t11=s.index(item2)
        dic_ret["职业"]=s[t10+2:t11].strip("_,")
    else:
        dic_ret["职业"]=None
    pattern = re.compile(r"(\d{1})")
    pattern2=re.compile(u"[\u4E00-\u9FA5]") #匹配汉字
    dic5=dic_config['联系方式']
    item1=dic5['1'] #读取关键字
    if item1 in s:
        t12=s.index(item1)
        m=pattern.search(str(s[t12:])) #从'联系方式'后面开始匹配第一个数字作为号码
        if m: #匹配到数字，继续匹配数字后面的第一个汉字，作为号码结束位置
            index=m.start(0)
            m2=pattern2.search(str(s[t12+index:])) #匹配数字后面的第一个汉字。
            index2=m2.start(0)
            dic_ret["联系方式"]=s[t12+index:t12+index+index2].strip('_,')
        else:
            dic_ret["联系方式"]=None
    else:
        dic_ret["联系方式"]=None
    return dic_ret