#coding:utf8
import re
def chuan_huan_form(address):
    with open(address,encoding='utf8') as f: #20180305102605798
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n') #java转出来的txt开头有\ufeff，python直接读取报错。
            a.append(line)
    dic_ret={}
    for i in range(len(a)):
        if "根据" in a[i]:
            index_start=i
        if "接受传唤" in a[i] or "依法拘传" in a[i] :
            index_end=i
    s=''
    for i in range(index_start,index_end+1):
        s+=a[i]

    pattern = re.compile(r"(\d{4})")

    if '涉嫌' in s and '的犯罪' in s:
        t1=s.index('涉嫌')
        t2=s.index('的犯罪')
        dic_ret["罪名"]=s[t1+2:t2]
    else:
        dic_ret["罪名"]=None

    if '嫌疑人' in s and '(' in s:
        t3=s.index('嫌疑人')
        t4=s.index('(')
        dic_ret["嫌疑人"]=s[t3+3:t4]
    else:
        dic_ret["嫌疑人"]=None
    
    if '性别' in s:
        t5=s.index('性别')
        dic_ret["性别"]=s[t5+2:t5+3]
    else:
        dic_ret["性别"]=None

    if '出生日期' in s and "住址" in s:
        t6=s.index('出生日期')
        t7=s.index("住址")
        dic_ret["出生日期"]=s[t6+4:t7-1].strip("_")
    else:
        dic_ret["出生日期"]=None

    if ')' in s or "于" in s: #以')' 和关键字'于'定位地址最后位置。
        if ')' in s:
            t8=s.index(')')
        if '于' in s:
            t8=s.index('于')
        dic_ret["住址"]=s[t7+2:t8-1]
    elif re.findall(pattern,s[t7:]): #如果没有')' 和关键字'于'，则匹配后面的日期作为地址的紧跟字符。
        t9=s[t7:].index(re.findall(pattern,s[t7:])[0])
        dic_ret["住址"]=s[t7+2:t7+t9]
    else:
        dic_ret["住址"]=None
    
    return dic_ret