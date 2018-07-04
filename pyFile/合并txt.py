#coding:utf8
#按行读取两个txt文件，存入两个字典中，然后按每个用户号码合并进一个字典，再写入txt中。
import win_unicode_console #防止因print出现OS错误
win_unicode_console.enable()
dic_new={}
dic_old={}
dic_all={}
with open(u'C:/Users/xutao/Desktop/selectNum新_v3.txt',encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        if '/' in line:
            i=1
            num=line.split('/')[-1].split(':')[0]
            dic_new.update({str(num):{
            }
            })
        elif ':' in line:
            dic_new[num][str(i)]=str(line).split(':')[-1].rstrip('\n')
            i+=1
    #print(dic_new)

with open(u'C:/Users/xutao/Desktop/selectNum旧V3.txt',encoding='utf8') as f:
    lines = f.readlines()
    for line in lines:
        #print(line)
        if '/' in line:
            i=1
            num=line.split('/')[-1].split(':')[0]
            dic_old.update({str(num):{
            }
            })
        elif ':' in line:
            dic_old[num][str(i)]=str(line).split(':')[-1].rstrip('\n')
            i+=1
    #print(dic_old)
dic_all.update(dic_new)


for key_new in dic_new.keys():
    i=1
    tmp=[]
    for key_old in dic_old.keys():
        if key_new==key_old:
            #print("key:",key_new)
            #print(dic_new[key_new])
            #print(dic_old[key_old])
            for item_new in dic_new[key_new]:
                tmp.append(dic_new[key_new][item_new])
                #print(dic_new[key_new][item_new])
                #dic_all[key_new][str(i)]=dic_new[key_new][item_new]
            for item_old in dic_old[key_old]:
                if dic_old[key_old][item_old] not in tmp:
                    tmp.append(dic_old[key_old][item_old])
                #print(dic_old[key_old][item_old])
            for item in tmp:
                dic_all[key_new][str(i)]=item
                i+=1
            #dic_all.update(dic_old[key_old])

#print(dic_all)

with open(u'C:/Users/xutao/Desktop/selectNum_合并V3.txt','a+') as f:
    j=1
    for key in dic_all.keys():
        #print(key)
        i=1
        
        f.write('第'+str(j)+'个:'+str(key)+':\n')
        j+=1
        for item in dic_all[key]:
            #print(dic_all[key][item])
            f.write(str(i)+':'+dic_all[key][item]+'\n')
            i+=1
        f.write('\n')