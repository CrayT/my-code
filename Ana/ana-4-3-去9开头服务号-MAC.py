#--coding:utf-8--
'''
这个py改动了json读取按照制定格式读取，因为读取的文件名为数字+字符+汉字的组合，
在写入文件中，增加了按照文件名写入的方式（原先只是数字和英文字符），可以写入中文字符了。
其他地方没有改动，excel还是原先的，不支持4个*的号码读取。

3月10号：
针对含有汉字的文件名，分析过后文本框没有显示，解决：将文件名转码后再输出。
在select函数最后，增加判断final_select数组长度，长度为零则judgelist置0，但好像对文件夹形式，没什么卵用。。。

882行在写入时增加判断fileLength[]是否为0的条件，若为0，则写入empty。

进度条待完善，进度信息暂时无法在类外动态更新。

增加：处理完成弹框提示。
增加：在读取文件夹的时候，顺便读出文件的数量，在写入txt的时候，将处理的文件数量也一起写入。
增加：final_select_counts，用来写入选出号码的通话次数。
增加：单个文件如果处理出错写入error
增加：读取excel文件，含有****号的号码也能读入
增加：json文件跳过400号码

3-13号51现场调试，包括csv和excel：
excel处理，包括有些号码乱码，导致出错，增加try报错机制。
4-4: 根据通话次数、主被叫、节假日次数、通话前后日期差来判断该机主号码是否为小号。
7-4： 266行通过号码开头数字9去除服务号码
'''
import sys
import os
import pandas as pd
import json
import numpy
import numpy as np
import time
from xlrd import xldate_as_tuple
import datetime
from datetime import datetime,date
from openpyxl import load_workbook
from xlrd import open_workbook
from wx import *
from phone_info_v3 import read_file
import traceback

def getFileList(path): #获取指定目录下的所有文件
    #filelist=[] #存放文件名
    files=os.listdir(path)
    for file in files:
        if file[0]=='.': #跳过隐藏文件
            continue
        elif file.endswith(('json','csv','txt','xls','xlsx')): #定义需要读取的文件类型
            filelist.append(path+'/'+file) #MAC和win此处不同
    #print filelist
    return filelist
#path='/Users/xutao/Downloads/Python/data_set/phonedata_zhang/'
#path=Path
#恢复号码区号：
def phone_recover(phone_before,phone_after):
    for i in range(len(phone_before)):
        if len(str(phone_before[i]))<11: #手机号不处理
            for item in phone_after:
                if str(phone_before[i]) in str(item) and len(str(phone_before[i]))<len(str(item)):
                    print(item)
                    phone_before[i]=item
def select(address):
    dateGap=120
    num=10
    fe=5
    Type=10
    try:
        if num_Get:
            num_get=int(num_Get) #若有定义输入，则用定义，否则默认为5个
    except:
        num_get=5
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
            #print "hello",year
            #print item
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
            #dial=MessageDialog(None,"时间数据格式-有误，请参照File-help！")
            judgelist.append(0) #处理出错，置0
            string=str(address)+"time数据格式有误，请参照File-help！"
            dial=MessageDialog(None,string)
            dial.ShowModal()
            exit()
    
    #找出所有通话记录的第一天和最后一天的天数之差：
    dic_ceshi = {}
    start_time2 = []
    for i in start_time:
        start_time2.append(i + ':00')
    result = sorted(start_time2, key=lambda date: datetime.strptime(date,"%Y-%m-%d %H:%M:%S"), reverse=True)
    lastday = result[0]
    firstday = result[len(result) - 1]
    year = lastday.split('-')[0]
    month = lastday.split('-')[1]
    day =  lastday.split('-')[2][0:2]
    year1 = firstday.split('-')[0]
    month1 = firstday.split('-')[1]
    day1 =  firstday.split('-')[2][0:2]
    day_cha = (datetime(int(year),int(month),int(day)) - datetime(int(year1),int(month1),int(day1))).days
    
    phonelist=[]
    dic_phone_festival={}  #每个号码的节假日附近通话次数
    dic_allPhone={} #所有号码的节假日附近的通话次数，及该机主的通话次数
    dic_phone_type={} #主被叫
    bj=0
    zj=0
    #判断该机主的通话日期，通话次数，节假日次数，主被叫情况，筛选短号,通过对键值置0或1来判断是否符合：
    dic_allPhone.update({
            "dateGap":0, #日期间隔
            "num":0, #通话次数
            "fes":0, #节假日
            "type":0 #主被叫
        })
    for item in other_cell_phone:#添加进每个文件的号码
        if item in phonelist:
            pass
        else:
            phonelist.append(item)
    for i in range(len(phonelist)):
        #dic_phone_use_time.update({phonelist[i]:0})
        dic_phone_festival.update({phonelist[i]:0}) #把特殊假期加到一起。
        dic_phone_type.update({phonelist[i]:
        {
            '被叫':bj,
            '主叫':zj
        }})
    type_zhu=0
    type_bei=0
    #print(init_type)
    for i in range(len(init_type)):
            try:
                if str(init_type[i])=='主叫':
                    type_zhu+=1
                    #dic_phone_type[other_cell_phone[i]]['主叫']=int(dic_phone_type[other_cell_phone[i]]['主叫'])+1
                else:
                    type_bei+=1
                    #dic_phone_type[other_cell_phone[i]]['被叫']=int(dic_phone_type[other_cell_phone[i]]['被叫'])+1
            except:
                pass


    special_festival=['1.01','1.02','5.01','4.30','5.02','12.29','12.28','12.27','12.26','12.25','12.24','4.04','5.14','6.18','9.15','10.04','10.01','10.02','10.03','9.30','9.29',] #考虑的节日日期,以小数存储
    #统计特殊假期通话次数
    count=0 #所有号码在节假日通话次数之和！
    for i in range(len(start_date1)):
        if str('%.2f'%float(start_date1[i])) in special_festival:
            count+=1 
            #dic_phone_festival[other_cell_phone[i]]=int(dic_phone_festival[other_cell_phone[i]])+1
    #print(dic_phone_festival)
    dic_allPhone['num']=len(other_cell_phone)
    dic_allPhone['fes']=count
    dic_allPhone['dateGap']=day_cha
    dic_allPhone['type']=type_zhu
    # print("count:",count)
    # print("num:",len(other_cell_phone))
    # print("dateGap:",day_cha)
    # print("type:",type_zhu)
    print(dic_allPhone)
    #用day_count统计记录中出现的日期，每个日期只记录一次
    day_count=[]
    for item in start_date1:
        if(item in day_count):
            pass
        else:
            day_count.append(item)
    count=0
    dic={} #字典，存放号码和对应次数
    def dic_relation():
        for item in other_cell_phone:
            if(item in dic.keys()):
                dic[item]+=1
            else:
                dic[item]=1
    dic_relation()
    #建立词典，一个号码若每天都打电话，则标记为1，否则标记为比例：
    dic_phone_day={}
    dic_phone_work={}#统计工作日天数
    dic_phone_fev={}#节假日
    #先将全部置一。
    for item in other_cell_phone:
        if(item in dic_phone_day.keys()):
            pass
        else:
            dic_phone_day[item]=1
    for item in other_cell_phone:
            dic_phone_work[item]=1
    for item in other_cell_phone:
            dic_phone_fev[item]=1
    #统计每个号码的工作日电话数
    i=0
    #print(len(start_weekday),len(other_cell_phone),len(start_time))
    for item in dic_phone_work.keys():
        i=0
        j=0
        f=0
        for call in other_cell_phone:
            if (item==call):
                if(start_weekday[i]>=1 and start_weekday[i]<=5):
                    j+=1
                elif(start_weekday[i]>=6 and start_weekday[i]<=7):
                    f+=1
                else:
                    pass
            else:
                pass
            i+=1
        dic_phone_work[item]=j
        dic_phone_fev[item]=f
    dic_phone_ratio={} #存放通话通话比例
    i=1
    for item in dic_phone_day.keys(): #item为号码
        i+=1
        print(item)
        if item in dic_phone_ratio.keys():
            pass
        else:
            if len(item)>=8:
                dic_phone_ratio[item]=float(1.0*(dic_phone_fev[item]-dic_phone_work[item])/(dic_phone_fev[item]+dic_phone_work[item]))
    print("i:",i)
    #建立根据比例筛选出的号码词典：
    dic_phone_select1={}
    for day_Gap in range(10,55,5): #为保证找出指定个数的号码，这里调整通话天数，先要求平均至少10天通话一次，15天次之，然后最差35天一次
        for item in dic_phone_ratio.keys():
            if dic[item]>=(len(day_count)/day_Gap):
                dic_phone_select1[item]=dic_phone_ratio[item]
        if len(dic_phone_select1)>num_get:
            break
    dic_phone_select={}
    i=0
    for item in sorted(dic_phone_select1.items(), key = lambda asd:asd[1], reverse=True) :
        #print(item[0])
        if (len(item[0])<=9 and str(item[0]).startswith('0')) or str(item[0]).startswith('9') or len(str(item[0]))<=3: #去除服务号码
            pass
        else:
            if i<num_get: #取前10个
                dic_phone_select[item[0]]=dic_phone_ratio[item[0]]  #按照从大到小排序输出,python2.7中sorted之后出来的item是元祖格式，提取号码需要item[0],python3不是这样。
                i+=1
            else:
                break
    #如下代码作用：统计出所有号码通话天数，即若某天有通话(无论一天中通话多少次)，则加一，
    #print("1")
    for item in dic_phone_day.keys():
        j=0
        tmp=[]
        for call in other_cell_phone:
            if (item!=call):
                pass
                j+=1
            else:                                                                                                                                  
                if(start_date1[j] in tmp):
                    pass
                else:
                    tmp.append(start_date1[j])
                j+=1
        dic_phone_day[item]=len(tmp)
    #print("最多通话天数：",max(dic_phone_day.values()))
    most_related_num=max(dic_phone_day.items(),key=lambda x:x[1])[0]
    tmparray=[]
    for i in range(len(other_cell_phone)):
        if(start_hour[i]>=16   and start_weekday[i]>=5 and start_weekday[i]<=7 and len(other_cell_phone[i])>=8):# and other_cell_phone[i][0]!='0'): #过滤掉0开始的号码):
            if(other_cell_phone[i] in dic_phone_select.keys()):  
                if(other_cell_phone[i] in tmparray):
                    pass
                else:
                    tmparray.append(other_cell_phone[i])
    if most_related_num in dic_phone_select:
        i=0
        for item in sorted(dic_phone_select, key = lambda asd:asd[1], reverse=True):
            if i>=num_get:
                break
            elif item in tmparray:
                final_select_tmp.append(item)
                final_select_counts.append(dic[item])
                #final_select_ratio.append(dic_phone_ratio[item])
                i+=1
            else:
                pass
    else:
        i=0
        final_select_tmp.append(most_related_num)
        final_select_counts.append(dic[most_related_num])
        #final_select_ratio.append(dic_phone_ratio[most_related_num])
        for item in sorted(dic_phone_select, key = lambda asd:asd[1], reverse=True):
            if i>num_get:
                break
            elif item in tmparray:
                final_select_tmp.append(item)
                final_select_counts.append(dic[item])
                #final_select_ratio.append(dic_phone_ratio[item])
                i+=1
            else:
                pass
    phone_recover(final_select_tmp,phone_with_id)
    print(final_select_tmp)
    for item in final_select_tmp:
        final_select.append(item)
    filelength.append(len(final_select))  #保存当final_select的长度，也即识别出的号码的个数
    if len(final_select)==0:
        judgelist.append(0)
    else:
        #if dic_allPhone['dateGap']<dateGap or dic_allPhone['num']<num or dic_allPhone['fes']<count or dic_allPhone['type']<Type:
        if int(dic_allPhone['dateGap']<dateGap) + int(dic_allPhone['num']<num) + int(dic_allPhone['fes']<count)  + int(dic_allPhone['type']<Type) >2: #满足其中两项
            judgelist.append(2) #可能是小号
        else:
            judgelist.append(1)  #若在处理过程中能走到这一步，这说明没有出错，置1.

#根据address的文件名，调用对应解析函数
def get_function(path):
    global filelist #定义全局存储文件名的列表，定义在调用函数内部最前面。
    global filelength #全局变量，存放每个文件识别出的号码长度
    global judgelist  #存放每个文件夹内的文件在处理的时候是否出错，若出错，置0，否则置1.
    filelength=[]
    filelist=[] #存放文件名
    judgelist=[]
    if '.' in path:  #判断addressPath中是文件夹还是单个文件
        filelist.append(path)
    else:
        getFileList(path) #是文件夹，调用获取文件名函数
    global final_select #全局数组final_select放在for外面，用来可以保存文件夹的多个文件。
    global final_select_counts
    global final_select_ratio
    final_select_ratio=[]
    final_select=[]
    final_select_counts=[]   #存放通话次数
    i=1
    for item in filelist:
        print(str(i)+'进行中！')
        i+=1
        global other_cell_phone#定义全局数组，这样每次调用一个文件，都会产生新数组，防止不同文件相互叠加
        global phone_with_id
        global start_time
        global final_select_tmp
        global init_type
        init_type=[]
        final_select_tmp=[]
        phone_with_id=[]
        other_cell_phone=[]
        start_time=[]
        try:
            print(item)
            result=read_file(item)
            #print(result)
            #print(type(result['calls']))
            if len(result['calls'])==0 or result['calls']=='error':
                #print(result['calls'])
                print(item)
                judgelist.append(0) #处理出错，置0
                #string=str(item)+"电话数据格式有误，请参照File-help！"
                # dial=MessageDialog(None,string)
                # dial.ShowModal()
            else:
                for it in result['calls']:
                    #print(it['st'],it['phone'][0],it['phone'][1])
                    start_time.append(it['st'])
                    #init_type.append(it['it'])
                    other_cell_phone.append(it['phone'][1])
                    phone_with_id.append(it['phone'][0])
                select(item)
            #print(init_type)
        except:
            traceback.print_exc()
            judgelist.append(0) #处理出错，置0
        print(len(other_cell_phone),len(phone_with_id))

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self,None,-1,title="通话记录分析",pos=(100,100),size=(800,600))
        panel=Panel(self,-1)
        global cb
        #cb=1
        self.button1=Button(panel,-1,"打开文件",pos=(370,100))
        self.button2=Button(panel,-1,"RUN",pos=(370,200),size=(100,40))
        self.button3=Button(panel,-1,"写入文件",pos=(370,320),size=(100,40))
        self.button4=Button(panel,-1,"确定",pos=(300,150),size=(60,20))

        cb1=RadioButton(panel,-1,label="Sigle file",pos=(70,60)) #定义文件读取方式，单个or文件夹形式
        self.Bind(EVT_RADIOBUTTON,self.onClick,cb1)

        cb2=RadioButton(panel,-1,label="Folder File",pos=(150,60))
        self.Bind(EVT_RADIOBUTTON,self.onClick,cb2)

        self.button1.Bind(EVT_BUTTON,self.getMyPath)
        
        StaticText(panel,-1,"文件",pos=(70,100))
        text=TextCtrl(panel,-1,pos=(100,100),size=(250,20))
        self.__TextBox1=text

        StaticText(panel,-1,"请输入想要输出的号码个数：\n(默认为5-6个)",pos=(70,150))
        text_input=TextCtrl(panel,-1,pos=(230,150),size=(60,20))
        self.__TextBox3=text_input
        #print text_input

        self.button4.Bind(EVT_BUTTON,self.getInput)

        self.button2.Bind(EVT_BUTTON,self.run_file)

        StaticText(panel,-1,"输出",pos=(70,200))
        text_output=TextCtrl(panel,-1,pos=(100,200),style=TE_MULTILINE |  TE_READONLY,size=(250,200),) #多行显示&只读
       
        self.__TextBox2=text_output

        #self.gauge = Gauge(panel, range =20, pos=(0,520),size = (800, 25), style =  GA_HORIZONTAL)  #进度条，待完善。
        #self.Bind(EVT_BUTTON, self.run_file, self.button2)

        self.button3.Bind(EVT_BUTTON,self.get_write_path)

        StaticText(panel,-1,"Date:2018-3-30",pos=(680,500))
        self.InitUI() 
    
    def onClick(self,event):
        global cb
        cb=event.GetEventObject().GetLabel()
        #print "on:",event.GetEventObject().GetLabel()
        if str(event.GetEventObject().GetLabel())=="Folder File":
            cb=2
        else:
            cb=1
        #print "on after:",cb,type(cb)
    def getInput(self,event): #得到输入的号码个数
        self.__TextBox2.Clear()
        #self.__TextBox3.GetValue()
        global num_Get
        num_Get=self.__TextBox3.GetValue()
        #print num_Get
    def run_file(self,event):  #输出识别号码
        get_function(Path)    #调用识别文件函数
        #print(final_select)
        #phone_recover(final_select,phone_with_id) #调用处理区号函数
        dial=MessageDialog(None,"处理完成！")
        dial.ShowModal()
        print(final_select)
        global fileLength  #全局变量，因为在写入时还要用到。
        fileLength=[] #存储每个文件号码的个数
        
        fileLength.append(filelength[0]) #先存第一个，以为下面的for循环相当于跳过了第一个，所以在for之前先append第一个数据
        for i in range(len(filelength)-1):
            fileLength.append(filelength[i+1]-filelength[i])
        #print fileLength
        if cb==1:  #单个文件的输出方式
            i=1
            if len(filelength) == 0:
                judgelist.append(0) #处理出错，置0
                Path1 = Path.encode('utf8')
                Path1 = str(Path1)
            # Path = str(Path)
                string=Path1 + "数据格式有误，请参照File-help！"
                dial=MessageDialog(None,string) #报错同时报错文件名字和路径
                #dial=MessageDialog(None,"json数据格式有误，请参照File-help！")
                dial.ShowModal()
            for item in final_select:
                #print item
                self.__TextBox2.AppendText(str(i)+":")
                self.__TextBox2.AppendText(str(item)+'\n')
                i+=1
                #self.__TextBox2.AppendText("\n")
        else: #文件夹文件的输出方式，先输出文件名，再输出文件号码个数的号码
            i=0 #控制final_select
            j=0 #控制judgelist
            f=0 #控制filelist

            for item in filelist:          #还没写完。。。。。。！！！！！！！！！！！！
                #print type(item)
                #print item
                #item=item.encode("utf8")
                item=item.split('\\')[-1]
                #print "hello1"
                item=str(item)
                #print "hello2"
                self.__TextBox2.AppendText(item+":"+"\n")#输出文件名
                #print "hello3"
                if judgelist[j]==1: #当前文件没有错误，输出。
                    #print fileLength[f]
                    for k in range(int(fileLength[f])): #输出当前文件的号码长度个数，若当前文件在处理时出错，
                        self.__TextBox2.AppendText(str(k+1)+":"+str(final_select[i])+"\n")
                        i+=1 #finalselct后移
                    j+=1 #judgelist加1，
                    f+=1 #filelist加1
                elif judgelist[j]==2: #当前文件没有错误，输出。
                    #print fileLength[f]
                    for k in range(int(fileLength[f])): #输出当前文件的号码长度个数，若当前文件在处理时出错，
                        self.__TextBox2.AppendText(str(k+1)+":"+str(final_select[i])+"\n")
                        i+=1 #finalselct后移
                    j+=1 #judgelist加1，
                    f+=1 #filelist加1
                elif judgelist[j]==0:  #当前文件有误，跳过。
                    #pass
                    j+=1 #文件错误，judgelist加1，但filelist不动
    def InitUI(self):    #自定义的函数,完成菜单的设置  
        menubar = MenuBar()        #生成菜单栏  
        filemenu = Menu()        #生成一个菜单  
        qmi1 = MenuItem(filemenu,1, "help")     #生成一个help菜单项  
        qmi2 = MenuItem(filemenu,2, "Quit")  #quit项，id设为2，在bind中调用
        filemenu.AppendItem(qmi1)            #把菜单项加入到菜单中  
        filemenu.AppendItem(qmi2)  
        menubar.Append(filemenu, "&File")        #把菜单加入到菜单栏中  
        self.SetMenuBar(menubar)            #把菜单栏加入到Frame框架中  
        self.Bind(EVT_MENU, self.OnQuit, id=2)    #给菜单项加入事件处理，id=2  
        self.Bind(EVT_MENU, self.help_window, id=1)  #help窗口
        self.Show(True)        #显示框架  

    def OnQuit(self, e):    #自定义函数　响应菜单项　　  
        self.Close()

    def help_window(self,event): #定义help窗口
        dial=MessageDialog(None,"路径及文件名称不要出现中文.\ntxt、csv、xls文件请尽量使用如下数据格式：\n第一行的列名：\n通话日期:start_time,\n通话location:place,"\
        +"\n通话类型:init_type,\n对方号码：other_cell_phone,\n通话持续时间:use_time\n数据格式："\
        +"\n通话日期:****/**/** **:**:**,\n对方号码:************,"\
        +"\n通话持续时长:**:**:**\n"\
        +"json文件格式:\n[\n  {\n   'start_time':****/**/** **:**:**\n   'other_cell_phone':***********\n   'use_time':**:**:**\n"\
        +"   ......\n   }\n   ......\n]\n不一样的格式可能导致无法读取！\n如果确认格式没有问题，请确认文件中是否出现了乱码的空行。",pos=(10,10)) #测试用
        dial.ShowModal()

    def get_write_path(self,event):
        dlg = DirDialog(self,u"选择文件夹",style=DD_DEFAULT_STYLE)  
        if dlg.ShowModal() == ID_OK:  
            #print "1"
            global Topath #定义全局变量Path
            #下面三行代码是为了兼容中文路径。
            Topath=dlg.GetPath()
            #Topath=Topath.encode("gbk")
            Topath=str(Topath)

            #print Topath
            #print cb
            try:
                if cb==1:
                    filenamee=(Path.split('/')[-1]).split(".")[0] #获取读取的文件名，来作为写入文件名，MAC和window此处不同。

                    filename=str(filenamee)

                    writePath=str(Topath)+"/"+filename+'.txt'  #将完整路径转化为一个字符串，防止出错
                    print(writePath)
                    writePath2=writePath.split('/')[-1]  #提取出文件名
                    i=1
                    with open(str(writePath),'a+') as f: #MAC和window此处不同。
                        f.write(str(writePath2)+":"+"\n")

                        if judgelist[0]==1:
                            for indexx in range(len(final_select)):  
                                #同时写入次数
                                #f.write(str(i)+":"+str(final_select[indexx])+" calls:"+str(final_select_counts[indexx])+" ration:"+str(final_select_ratio[indexx])+'\n') #将筛选号码写入txt
                                f.write(str(i)+":"+str(final_select[indexx])+'\n') #将筛选号码写入txt
                                i+=1
                            f.write('\n')
                        elif judgelist[0]==2:
                            f.write("<<<此号可能是小号！>>>"+'\n')
                            for indexx in range(len(final_select)):  
                                #同时写入次数
                                #f.write(str(i)+":"+str(final_select[indexx])+" calls:"+str(final_select_counts[indexx])+" ration:"+str(final_select_ratio[indexx])+'\n') #将筛选号码写入txt
                                f.write(str(i)+":"+str(final_select[indexx])+'\n') #将筛选号码写入txt
                                i+=1
                            f.write('\n')
                        else:
                            f.write("error")  #单个文件如果处理出错写入error。
                    dial=MessageDialog(None,"写入成功！")
                    dial.ShowModal()
                   # return Topath #文件夹路径  
                else:
                    print(Path)
                    #dir_name=Path.split('\\')[-2] #获得文件夹名字
                    #print(dir_name)
                    with open(Topath+'/selectNum.txt','a+') as fw: #竟然不能命名为f！！调试了半天没有发现哪里错误。。。MAC和window此处不同。
                    #with open(Topath+'\\'+str(dir_name)+'.txt','a+') as fw: #以文件夹名字命名txt。
                        fw.write(str(Topath)+':'+'\n')
                        #print fileNum
                        fw.write("Total files number:"+str(fileNum)+"\n"+"\n")
                        fw.flush()
                        i=0 #控制final_select
                        j=0 #控制judgelist
                        f=0 #控制filelist
                        for item in filelist:
                            #print item
                            filenamee=(item.split("/")[-1]).split(".")[0] #MAC和window此处不同。
                            #filename=filenamee.encode("gbk")
                            filename=str(filenamee)
                            fw.write(str(filename)+':'+'\n') 
                            #self.__TextBox2.AppendText(str(item)+"\n")#输出文件名
                            if judgelist[j]==1: #当前文件没有错误，输出。

                                if(int(fileLength[f])==0):  #若某个文件为空，或不为空，但数据太少导致分析出的号码数组为空，则fileLength[f]就会为0，此时写入empty。不然会什么都不写。
                                    fw.write("empty."+"\n")
                                else:
                                    for k in range(int(fileLength[f])): #输出当前文件的号码长度个数，若当前文件在处理时出错，
                                        #fw.write(str(k+1)+":"+str(final_select[i])+" calls:"+str(final_select_counts[i])+" ratio:"+str(final_select_ratio[i])+"\n")  #写次数
                                        fw.write(str(k+1)+":"+str(final_select[i])+"\n")
                                        i+=1 #finalselct后移
                                fw.write('\n')
                                j+=1 #judgelist加1
                                f+=1 #filelist加1
                            elif judgelist[j]==2: #当前文件没有错误，输出。
                                fw.write("<<<此号可能是小号！>>>"+'\n')
                                if(int(fileLength[f])==0):  #若某个文件为空，或不为空，但数据太少导致分析出的号码数组为空，则fileLength[f]就会为0，此时写入empty。不然会什么都不写。
                                    fw.write("empty."+"\n")
                                else:
                                    for k in range(int(fileLength[f])): #输出当前文件的号码长度个数，若当前文件在处理时出错，
                                        #fw.write(str(k+1)+":"+str(final_select[i])+" calls:"+str(final_select_counts[i])+" ratio:"+str(final_select_ratio[i])+"\n")  #写次数
                                        fw.write(str(k+1)+":"+str(final_select[i])+"\n")
                                        i+=1 #finalselct后移
                                fw.write('\n')
                                j+=1 #judgelist加1
                                f+=1 #filelist加1
                            elif judgelist[j]==0:  #当前文件有误，写入error。
                                fw.write('error!'+'\n'+'\n')
                                j+=1 #文件错误，judgelist加1，但filelist不动
                        dial=MessageDialog(None,"写入成功！")
                        dial.ShowModal()
            except:
                #print "error!"
                dial=MessageDialog(None,"not all files succeed!")
                dial.ShowModal()
        dlg.Destroy()

    def getMyPath(self,event):
        #print "final cb:",cb
        self.__TextBox2.Clear()  #清除文本框
        global Path #定义全局变量Path
        if cb==2:
            dlg=DirDialog(self,"选择文件夹",style=DD_DEFAULT_STYLE)
            if dlg.ShowModal() == ID_OK:  
                
                Path=dlg.GetPath()
                self.__TextBox1.SetLabel(Path) #设置textbox内容为文件内容
                global fileNum
                fileNum=0
                for lists in os.listdir(Path):                     # 统计文件数量
                    sub_path = os.path.join(Path, lists)
                    #print(sub_path)
                    if os.path.isfile(sub_path):
                        fileNum = fileNum+1  
                return Path #文件夹路径
            dlg.Destroy() 
        else:
            dlg = FileDialog(self,u"选择文件",style=DD_DEFAULT_STYLE)  
            if dlg.ShowModal() == ID_OK:  
                Path=dlg.GetPath()
                self.__TextBox1.SetLabel(Path) #设置textbox内容为文件内容
                return Path #文件夹路径       
            dlg.Destroy() 

if __name__ == "__main__":
    app = App()    #创建应用的对象
    myframe = MyFrame()    #创建一个自定义出来的窗口
    #myframe.Center()#正中间显示
    myframe.Show()    #这两句一定要在MainLoop开始之前就执行    
    app.MainLoop()