#--coding:utf-8--
'''
7-27: 综合新旧模型，旧模型使用15个号码的前5个，新模型使用 申请日前6个月内最近一次呼出距离申请日天数 一个指标为10.18的，进行合并输出。
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
from wx import *
from phone_info_v3 import read_file
import traceback
from ana_old_tmp import get_function_old
from ana_new_tmp import get_function_new
from function import get_desktop

def log(mess):  #在当前文件夹下写入日志文件
    m=datetime.now().month
    d=datetime.now().day
    n='ana_pro_'+str(m)+"-"+str(d)
    with open(str(n)+'.log','a+',encoding='utf8') as f:
        f.write(str(mess)+str(datetime.now())+'\n')

def getFileList(path): #获取指定目录下的所有文件
    files=os.listdir(path)
    for file in files:
        if file[0]=='.': #跳过隐藏文件
            continue
        elif file.endswith(('json','csv','txt','xls','xlsx')): #定义需要读取的文件类型
            filelist.append(path+'/'+file) #MAC和win此处不同
    return filelist

#恢复号码区号：
def phone_recover(phone_before,phone_after):
    for i in range(len(phone_before)):
        if len(str(phone_before[i]))<11: #手机号不处理
            for item in phone_after:
                if str(phone_before[i]) in str(item) and len(str(phone_before[i]))<len(str(item)):
                    print(item)
                    phone_before[i]=item

def select(address):
    log("start to select...")
    try:
        if num_Get:
            num_get=int(num_Get) #若有定义输入，则用定义，否则默认为5个
    except:
        num_get=5
    file_name=address.split('/')[-1].split('.')[0].split('/')[-1]
    print(file_name)

    log("调取旧模型 开始")
    list_num_old,list_ratio,list_counts=get_function_old(address,num_get)
    log("调取旧模型 结束")

    log("调取新模型 开始")
    list_num_new,list_1,list_2,list_3,list_4,list_5,list_6,list_7,list_8=get_function_new(address,num_get)
    log("调取新模型 结束")

    phone_recover(list_num_old,phone_with_id) #恢复区号
    phone_recover(list_num_new,phone_with_id) #恢复区号

    print('旧 list_num_old:',list_num_old)
    print('新 list_num_new:',list_num_new)

    #截取list_num_old前5个：
    list_num_tmp=list_num_old[:5]
    print("旧模型前5个号码:",list_num_tmp)

    #获取list_num_1中list_7中为10.18的号码：
    list_num_1_tmp=[]
    for i in range(len(list_num_new)):
        if list_7[i]==10.184982602:
            list_num_1_tmp.append(list_num_new[i])
    print("新模型 提取号码:",list_num_1_tmp)

    with open('output.txt','a+') as f:  #在代码的当前文件夹写入txt文件
        f.write(str(file_name)+":"+"\n")
        log("准备写入txt...")
        k=1
        try:
                log("开始写入txt...")
                log(str(file_name))
                for i in range(len(list_num_tmp)):  
                    f.write(str(k)+"-:"+str(list_num_tmp[i])+'\n')  #旧号码序号后面达标记:"-"
                    k+=1
                    
                for i in range(len(list_num_1_tmp)):  
                    if list_num_1_tmp[i] not in list_num_tmp:
                        f.write(str(k)+":"+str(list_num_1_tmp[i])+'\n')
                        k+=1
                f.write("\n")

                log("写入txt结束...")
            
        except Exception as e:
            print(e)
            f.write("encounter error"+str(e)+'\n')
        log("写入txt +1!..."+'\n')
    log("写入txt完成!..."+'\n')
    print("处理完成！")

#根据address的文件名，调用对应解析函数
def get_function(path):
    global filelist #定义全局存储文件名的列表，定义在调用函数内部最前面。
    global filelength #全局变量，存放每个文件识别出的号码长度
    global judgelist  #标记数组，存放每个文件夹内的文件在处理的时候是否出错，若出错，置0，否则置1.
    global final_select_counts
    global final_select_ratio
    filelength=[]
    filelist=[] #存放文件名
    judgelist=[]
    if '.' in path:  #判断addressPath中是文件夹还是单个文件
        filelist.append(path)
    else:
        getFileList(path) #是文件夹，调用获取文件名函数
    
    final_select_ratio=[]
    final_select_counts=[]   #存放通话次数
    log("get_function start..")
    i=1
    for item in filelist:
        print("正在处理第"+str(i)+"个！")
        i+=1
        log(str(item))
        global other_cell_phone#定义全局数组，前后调用；for下面定义，每次调用一个文件，都会产生新数组，防止不同文件相互叠加
        global phone_with_id
        global start_time
        global init_type
        init_type=[]
        phone_with_id=[]
        other_cell_phone=[]
        start_time=[]
        try:
            print(item)
            result=read_file(item) #调用读取文件函数
            if len(result['calls'])==0 or result['calls']=='error':
                log("获取calls 失败...")
                judgelist.append(0) #处理出错，置0
                string=str(item)+"电话数据格式有误，请参照File-help！"
            else:
                log("获取calls成功...")
                for it in result['calls']:
                    start_time.append(it['st']) # start_time
                    init_type.append(it['it'])  #主被叫
                    other_cell_phone.append(it['phone'][1]) #不带区号
                    phone_with_id.append(it['phone'][0])  #带区号
                select(item) #拿到数据后开始进行分析，参数为单个文件地址
        except Exception as e:
            log(str(e))
            traceback.print_exc()
            judgelist.append(0) #处理出错，置0

class MyFrame(Frame):
    def __init__(self):
        Frame.__init__(self,None,-1,title="通话记录分析",pos=(100,100),size=(800,600))
        panel=Panel(self,-1)
        self.button1=Button(panel,-1,"打开文件",pos=(370,100))
        self.button2=Button(panel,-1,"RUN",pos=(370,200),size=(100,40))
        #self.button3=Button(panel,-1,"写入文件",pos=(370,320),size=(100,40))  #隐藏写入文件按钮
        self.button4=Button(panel,-1,"确定",pos=(300,150),size=(60,20))

        cb1=RadioButton(panel,-1,label="Sigle file",pos=(70,60)) #定义文件读取方式，单个
        self.Bind(EVT_RADIOBUTTON,self.onClick,cb1)

        cb2=RadioButton(panel,-1,label="Folder File",pos=(150,60)) #定义文件夹读取方式，文件夹形式
        self.Bind(EVT_RADIOBUTTON,self.onClick,cb2)

        self.button1.Bind(EVT_BUTTON,self.getMyPath)
        
        StaticText(panel,-1,"文件",pos=(70,100))
        text=TextCtrl(panel,-1,pos=(100,100),size=(250,20))
        self.__TextBox1=text
        StaticText(panel,-1,"请输入想要输出的号码个数：\n(默认为5-6个)",pos=(70,150))
        text_input=TextCtrl(panel,-1,pos=(230,150),size=(60,20))
        self.__TextBox3=text_input
        self.button4.Bind(EVT_BUTTON,self.getInput)
        self.button2.Bind(EVT_BUTTON,self.run_file)
        StaticText(panel,-1,"输出",pos=(70,200))
        text_output=TextCtrl(panel,-1,pos=(100,200),style=TE_MULTILINE |  TE_READONLY,size=(250,200),) #多行显示&只读
        self.__TextBox2=text_output
        #self.button3.Bind(EVT_BUTTON,self.get_write_path) 
        StaticText(panel,-1,"Date:2018-4-17",pos=(680,500))
        self.InitUI() 
    
    def onClick(self,event):
        global cb #文件or文件夹标记
        cb=event.GetEventObject().GetLabel()
        if str(event.GetEventObject().GetLabel())=="Folder File":
            cb=2
        else:
            cb=1
    def getInput(self,event): #得到输入的号码个数
        log("get input...")
        self.__TextBox2.Clear()
        global num_Get
        num_Get=self.__TextBox3.GetValue()
    def run_file(self,event):  #输出识别号码
        log("start to run...")
        get_function(Path)    #调用识别文件函数
        log("get_function end...")
        dial=MessageDialog(None,"处理完成！")
        dial.ShowModal()
        #下面注释的是之前写的将结果写入textbox内的代码，实际没什么作用，而且容易出错，注释掉。
        ''' 
        global fileLength  #全局变量，因为在写入时还要用到。
        fileLength=[] #存储每个文件号码的个数
        fileLength.append(filelength[0]) #先存第一个，以为下面的for循环相当于跳过了第一个，所以在for之前先append第一个数据
        for i in range(len(filelength)-1):
            fileLength.append(filelength[i+1]-filelength[i])
        if cb==1:  #单个文件的输出方式
            log("单个文件输出至textbox...")
            i=1
            if len(filelength) == 0:
                judgelist.append(0) #处理出错，置0
                Path1 = Path.encode('utf8')
                Path1 = str(Path1)
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
            log("单个文件输出至textbox 成功...")
        else: #文件夹文件的输出方式，先输出文件名，再输出文件号码个数的号码
            log("多个文件输出至textbox...")
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
            log("多个文件输出至textbox 成功...")
        '''
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
        log("获取写入文件夹...")
        dlg = DirDialog(self,u"选择文件夹",style=DD_DEFAULT_STYLE)  
        if dlg.ShowModal() == ID_OK:  
            #print "1"
            global Topath #定义全局变量Path
            #下面三行代码是为了兼容中文路径。
            Topath=dlg.GetPath()
            Topath=str(Topath)
            log("获取文件夹成功...")
            log(str(Topath))
            try:
                if cb==1:
                    log("单个文件开始写入...")
                    filenamee=(Path.split('\\')[-1]).split(".")[0] #获取读取的文件名，来作为写入文件名，MAC和window此处不同。
                    filename=str(filenamee)
                    writePath=str(Topath)+"\\"+filename+'.txt'  #将完整路径转化为一个字符串，防止出错
                    print(writePath)
                    writePath2=writePath.split('\\')[-1]  #提取出文件名
                    i=1
                    with open(str(writePath),'a+') as f: #MAC和window此处不同。
                        f.write(str(writePath2)+":"+"\n")
                        log("单个文件开始写入txt...")
                        if judgelist[0]==1:
                            for indexx in range(len(final_select)):  
                                #同时写入次数
                                #f.write(str(i)+":"+str(final_select[indexx])+" calls:"+str(final_select_counts[indexx])+" ration:"+str(final_select_ratio[indexx])+'\n') #将筛选号码写入txt
                                #f.write(str(i)+":"+str(final_select[indexx])+'\n') #将筛选号码写入txt
                                f.write(str(i)+":"+str(final_select[indexx])+'  '+str(dic_ratio[final_select[indexx]])+'\n')
                                i+=1
                            f.write('\n')
                        elif judgelist[0]==2:
                            f.write("<<<此号可能是小号！>>>"+'\n')
                            for indexx in range(len(final_select)):  
                                #同时写入次数
                                #f.write(str(i)+":"+str(final_select[indexx])+" calls:"+str(final_select_counts[indexx])+" ration:"+str(final_select_ratio[indexx])+'\n') #将筛选号码写入txt
                                #f.write(str(i)+":"+str(final_select[indexx])+'\n') #将筛选号码写入txt
                                f.write(str(i)+":"+str(final_select[indexx])+'  '+str(dic_ratio[final_select[indexx]])+'\n')
                                i+=1
                            f.write('\n')
                        else:
                            f.write("error")  #单个文件如果处理出错写入error。
                    dial=MessageDialog(None,"写入成功！")
                    dial.ShowModal()
                    log("单个文件写入成功...")
                    return Topath #文件夹路径  
                else:
                    log("开始写入多个文件...")
                    with open(Topath+'\\selectNum.txt','a+') as fw: #竟然不能命名为f！！调试了半天没有发现哪里错误。。。MAC和window此处不同。
                        fw.write(str(Topath)+':'+'\n')
                        #print fileNum
                        fw.write("Total files number:"+str(fileNum)+"\n"+"\n")
                        fw.flush()
                        i=0 #控制final_select
                        j=0 #控制judgelist
                        f=0 #控制filelist
                        log("开始写入多个文件至txt...")
                        for item in filelist:
                            #print item
                            filenamee=(item.split("\\")[-1]).split(".")[0] #MAC和window此处不同。
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
                                        #fw.write(str(k+1)+":"+str(final_select[i])+"\n")
                                        fw.write(str(k+1)+":"+str(final_select[i])+'    '+str(dic_ratio[final_select[i]])+"\n")
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
                                        fw.write(str(k+1)+":"+str(final_select[i])+'    '+str(dic_ratio[final_select[i]])+"\n")
                                        i+=1 #finalselct后移
                                fw.write('\n')
                                j+=1 #judgelist加1
                                f+=1 #filelist加1
                            elif judgelist[j]==0:  #当前文件有误，写入error。
                                fw.write('error!'+'\n'+'\n')
                                j+=1 #文件错误，judgelist加1，但filelist不动
                        dial=MessageDialog(None,"写入成功！")
                        dial.ShowModal()
                        log("多个文件写入成功...")
            except Exception as e:
                log(str(e))
                dial=MessageDialog(None,"not all files succeed!")
                dial.ShowModal()
        dlg.Destroy()

    def getMyPath(self,event):
        log("start get path...")
        self.__TextBox2.Clear()  #清除文本框
        global Path #定义全局变量Path，文件夹路径
        if cb==2:
            dlg=DirDialog(self,"选择文件夹",style=DD_DEFAULT_STYLE)
            if dlg.ShowModal() == ID_OK:  
                Path=dlg.GetPath()
                self.__TextBox1.SetLabel(Path) #设置textbox内容为文件内容
                global fileNum
                fileNum=0
                for lists in os.listdir(Path):                     # 统计文件数量
                    sub_path = os.path.join(Path, lists)
                    if os.path.isfile(sub_path):
                        fileNum = fileNum+1  
                return Path #文件夹路径
            dlg.Destroy() 
        else:
            dlg = FileDialog(self,u"选择文件",style=DD_DEFAULT_STYLE)  
            if dlg.ShowModal() == ID_OK:  
                Path=dlg.GetPath()
                self.__TextBox1.SetLabel(Path) #设置textbox内容为文件内容
                return Path        
            dlg.Destroy() 
        log("get path done...")
if __name__ == "__main__":
    app = App()    #创建应用的对象
    myframe = MyFrame()    #创建一个自定义出来的窗口
    #myframe.Center()#正中间显示
    myframe.Show()    #这两句一定要在MainLoop开始之前就执行    
    app.MainLoop()