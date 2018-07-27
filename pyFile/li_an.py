#coding:utf8

def li_an_form(address):
    with open(address,encoding='utf8') as f: #20180305102605798
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n') #java转出来的txt开头有\ufeff，python直接读取报错。
            a.append(line)
    
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
    if '《' in s and '》' in s:
        t1=s.index('《')
        t2=s.index('》')
        dic_ret["法律"]=s[t1:t2+1]
    else:
        dic_ret["法律"]=None
    if '第' in s and '条' in s:
        t3=s.index('第')
        t4=s.index('条')
        dic_ret["第条"]=s[t3+1:t4+1]
    else:
        dic_ret["第条"]=None
    if '对' in s and '对' in s:
        t5=s.index('对')
        t6=s.index('立')
        dic_ret["罪名"]=s[t5+1:t6]
    else:
        dic_ret["罪名"]=None


    
    return dic_ret