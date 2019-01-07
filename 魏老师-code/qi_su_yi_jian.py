#coding:utf8
import json
def qi_su_yi_jian(address):
    with open(address,encoding='utf8') as f: #20180305102605798
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n')
            a.append(line)
    with open("config.json",'r',encoding='utf8') as f: #ubuntu
            config = json.load(f)
    dic_config=config['起诉意见'] #读取配置文件的关键字
    dic_ret={}
    key_start_end=dic_config['start_end']
    key_start=key_start_end['1']
    key_end=key_start_end['2']
    for i in range(len(a)):
        if key_start in a[i]: #查找开始位置。
            index_start=i
            break
    for i in range(len(a)):
        if key_end in a[i]: #查找末尾位置。
            index_end=i
            break
    key_word=dic_config['key_word'] #提取关键字
    key1=key_word['1'] #违法犯罪 ，这个文档中不一定有。
    key2=key_word['2'] #一案
    key3=key_word['3'] #经依法侦查
    key4=key_word['4'] #认定上述犯罪 ,不一定是这个关键字
    key4_2=key_word['4-2']
    key5=key_word['5'] #上述犯罪事实,不一定有。
    key6=key_word['6'] #综上所述
    #匹配出以"犯罪嫌疑人"开始的行标，可能有多个犯罪嫌疑人，需要把下标都找到。
    key_start_index=[]
    for i in range(len(a)):
        if a[i].startswith(key_start):
            key_start_index.append(i)
    #匹配出"违法犯罪"的行标，不一定有
    key_1=-1
    key_2=-1
    key_3=-1
    key_4=-1
    key_5=-1
    key_6=-1
    flag1=False
    flag2=False
    flag3=False
    flag4=False
    flag5=False
    flag6=False
    for i in range(len(a)):
        if not flag1: #违法犯罪
            if a[i].startswith(key1):
                key_1=i
                flag1=True
        if not flag2: #一案,这个是行中文字含有该关键字。
            if key2 in a[i]:
                key_2=i
                flag2=True
        if not flag3: #经依法侦查
            if key3 in a[i]:
                key_3=i
                flag3=True
        if not flag4: #认定上述犯罪
            if a[i].startswith(key4) or a[i].startswith(key4_2):
                key_4=i
                flag4=True
        if not flag5: #上述犯罪事实
            if a[i].startswith(key5):
                key_5=i
                flag5=True
        if not flag6: #综上所述
            if a[i].startswith(key6):
                key_6=i
                flag6=True
    # print(index_start,index_end,key_start_index)
    # print(key_1,key_2,key_3,key_4,key_5,key_6,)

    s1=''
    if key_1>0 and key_2>0:
        for i in range(key_1,key_2):
            s1+=a[i]
        if "无" in s1:
            dic_ret['犯罪经历']="None"
        else:
            dic_ret['犯罪经历']=s1
    else:
        dic_ret['犯罪经历']="None"

    dic_ret['犯罪嫌疑人']={}
    key_tmp=key_1 if key_1>0 else key_2  #key_1>0: 存在犯罪经历描述
    list_tmp=key_start_index
    if key_tmp not in list_tmp:
        list_tmp.append(key_tmp)
    list_tmp=sorted(list_tmp)
    for i in range(len(list_tmp)): #Perfect！怎么能想到用这么简单的方法处理，哈哈！
        s=''
        if list_tmp[i]<key_tmp:
            for k in range(list_tmp[i],list_tmp[i+1]):
                s+=a[k]
            dic_ret['犯罪嫌疑人'].update({str(i+1):s})
    s=''
    index_tmp=key_5 if key_5>0 else key_6
    if key_4>0:
        for i  in range(key_4,index_tmp):
            s+=a[i]
        dic_ret['证据']=s
    else:
        dic_ret['证据']="None"

    s=''
    if key_5>0 and key_6>0:
        for i  in range(key_5,key_6):
            s+=a[i]
        dic_ret['犯罪事实']=s
    else:
        dic_ret['犯罪事实']="None"

    s=''
    if key_6>0:
        index_tmp=key_5 if key_5>0 else key_4
        for i  in range(key_6,index_end):
            s+=a[i]
        dic_ret['综上所述']=s
    else:
        dic_ret['综上所述']="None"

    s=''
    if key_3>0 and key_4 >0:
        for i  in range(key_3,key_4):
            s+=a[i]
        dic_ret['查明']=s
    else:
        dic_ret['查明']="None"
    return dic_ret