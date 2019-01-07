#coding:utf8
import json
def juan_zong(address):
    with open(address,encoding='utf8') as f: #20180305102605798
        lines = f.readlines()
        a=[]
        for line in lines:
            line=line.encode('utf-8').decode('utf-8-sig').strip('\n')
            a.append(line)
    with open("config.json",'r',encoding='utf8') as f: #ubuntu
            config = json.load(f)
    dic_config=config['卷宗'] #读取配置文件的关键字
    dic_ret={}
    list_1=[]
    list_2=[]
    list_3=[]
    list_4=[]
    list_5=[]
    list_6=[]
    list_7=[]
    list_8=[]
    list1=sorted(dic_config["1"].items(), key = lambda asd:asd[1], reverse=True)
    list2=sorted(dic_config["2"].items(), key = lambda asd:asd[1], reverse=True)
    list3=sorted(dic_config["3"].items(), key = lambda asd:asd[1], reverse=True)
    list4=sorted(dic_config["4"].items(), key = lambda asd:asd[1], reverse=True)
    list5=sorted(dic_config["5"].items(), key = lambda asd:asd[1], reverse=True)
    list6=sorted(dic_config["6"].items(), key = lambda asd:asd[1], reverse=True)
    list7=sorted(dic_config["7"].items(), key = lambda asd:asd[1], reverse=True)
    list8=sorted(dic_config["8"].items(), key = lambda asd:asd[1], reverse=True)
    for i in range(len(list1)):
        list_1.append(list1[i][1])
    for i in range(len(list2)):
        list_2.append(list2[i][1])
    for i in range(len(list3)):
        list_3.append(list3[i][1])
    for i in range(len(list4)):
        list_4.append(list4[i][1])
    for i in range(len(list5)):
        list_5.append(list5[i][1])
    for i in range(len(list6)):
        list_6.append(list6[i][1])
    for i in range(len(list7)):
        list_7.append(list7[i][1])
    for i in range(len(list8)):
        list_8.append(list8[i][1])
    list_all=[]
    list_4_5=[]  #结案时间和立案时间单独处理
    list_all.append(list_1)
    list_all.append(list_2)
    list_all.append(list_3)
    list_4_5.append(list_4)
    list_4_5.append(list_5)
    list_all.append(list_6)
    list_all.append(list_7)
    list_all.append(list_8)

    for list_tmp in list_all: #根据配置文件的关键字自动顺序匹配，一旦匹配成功就跳出。
        flag_break=False
        index_tmp=-1
        item_tmp=list_tmp[0]
        for item1 in list_tmp:
            for item_2 in a:
                if item1 in item_2:
                    index_tmp=a.index(item_2)
                    if len(a[index_tmp])>len(item1)+1: #若本行后面没有内容，则默认下一行为需要内容
                        dic_ret[item1]=a[index_tmp][len(item1):].strip(":_")
                    else:
                        dic_ret[item1]=a[index_tmp+1].strip(":_")
                    flag_break=True
                    break
                if flag_break:
                    break
            if flag_break:
                    break
        if index_tmp<0:
            dic_ret[item_tmp]="None"

    for list_tmp in list_4_5: #因为时间是数字开始，所以这两个单独拿出来处理
        flag_break=False
        index_tmp=-1
        item_tmp=list_tmp[0]
        for item1 in list_tmp:
            for item_2 in a:
                if item1 in item_2:
                    index_tmp=a.index(item_2)
                    if len(a[index_tmp])>len(item1)+2:
                        dic_ret[item1]=a[index_tmp][len(item1):].strip(":_")
                    elif a[index_tmp+1][:4].isdigit(): #需要是4个数字开始才判断为是时间。
                        dic_ret[item1]=a[index_tmp+1].strip(":_")
                    else:
                        dic_ret[item1]="None"
                    flag_break=True
                    break
                if flag_break:
                    break
            if flag_break:
                    break
        if index_tmp<0:
            dic_ret[item_tmp]="None"
    return dic_ret