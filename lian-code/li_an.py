#coding:utf8
import json
def li_an_form(address):
    with open(address,encoding='utf8') as f: #20180305102605798
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n') #java转出来的txt开头有\ufeff，python直接读取报错。
            a.append(line)
    with open("config.json",'r',encoding='utf8') as f: #ubuntu
            config = json.load(f)
    dic_config=config['li_an'] #读取配置文件的关键字
    dic_ret={}
    dic_ret["公安局"]=a[0]
    for i in range(len(a)):
        if "根据" in a[i]:
            index_start=i
        if "立案侦查" in a[i]:
            index_end=i
    s=''
    for i in range(index_start,index_end+1):
        s+=a[i]
    
    dic1=dic_config['法律']
    item1=dic1['1'] #读取关键字
    item2=dic1['2']
    if item1 in s and item2 in s:
        t1=s.index(item1)
        t2=s.index(item2)
        dic_ret["法律"]=s[t1:t2+1]
    else:
        dic_ret["法律"]=None
    dic2=dic_config['第条']
    item1=dic2['1']
    item2=dic2['2']
    if item1 in s and item2 in s:
        t3=s.index(item1)
        t4=s.index(item2)
        dic_ret["第条"]=s[t3+1:t4+1]
    else:
        dic_ret["第条"]=None
    dic3=dic_config['罪名']
    item1=dic3['1']
    item2=dic3['2']
    if item1 in s and item2 in s:
        t5=s.index(item1)
        t6=s.index(item2)
        dic_ret["案件"]=s[t5+1:t6]
    else:
        dic_ret["案件"]=None
    return dic_ret