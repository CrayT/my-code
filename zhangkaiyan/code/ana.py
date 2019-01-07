#--coding:utf-8--
import sys
import os
import pandas as pd
import json
import numpy
import numpy as np
from xlrd import xldate_as_tuple
import datetime
from datetime import datetime,date
from wx import *
import  xlwt
import traceback
from collections import Counter 

def get_function(path,num):
    # print("num %s"%(num))
    data={}
    phone_list=[]
    with open(path,'r') as f:
        info=json.loads(f.read())
    temp=info['calls']
    for item in temp:
        phone_list.append(item['other_cell_phone'])
    phone=[]
    count=[]
    phone_tmp=[]
    count_tmp=[]
    try:
        data=Counter(phone_list)
        for item in sorted(data.items(), key = lambda asd:asd[1], reverse=True):
            phone.append(item[0])
            count.append(item[1])
        for i in range(len(phone)):
            if i<int(num):
                phone_tmp.append(phone[i])
                count_tmp.append(count[i])
            else:
                break
        # phone_tmp=phone[:int(num)]
        # count_tmp=count[:int(num)]
        # print(phone_tmp)
        # print(count_tmp)
        return phone_tmp,count_tmp

    except Exception as e:
        dial=MessageDialog(None,"process error")
        dial.ShowModal()
        traceback.print_exc()
        return 'error'
class MyFrame(Frame):
    def __init__(self):
        self.num_Get=5
        self.phone=[]
        self.count=[]
        Frame.__init__(self,None,-1,title="demo",pos=(100,100),size=(300,350))
        panel=Panel(self,-1)
        self.button1=Button(panel,-1,"open",pos=(100,100))
        self.button2=Button(panel,-1,"RUN",pos=(100,200),size=(100,40))
        self.button3=Button(panel,-1,"write",pos=(100,250),size=(100,40))  #隐藏写入文件按钮
        self.button4=Button(panel,-1,"sure",pos=(200,150),size=(60,20))
        self.button1.Bind(EVT_BUTTON,self.getMyPath)
        self.button3.Bind(EVT_BUTTON,self.get_write_path)

        StaticText(panel,-1,"output number:",pos=(50,150))
        text_input=TextCtrl(panel,-1,pos=(150,150),size=(40,20))
        self.__TextBox3=text_input
        self.button4.Bind(EVT_BUTTON,self.getInput)
        self.button2.Bind(EVT_BUTTON,self.run_file)

        self.InitUI() 
    


    def getInput(self,event):
        self.num_Get=self.__TextBox3.GetValue()
    def run_file(self,event):  #输出识别号码

        phone,count=get_function(Path,self.num_Get)    #调用识别文件函数
        print(phone)
        self.phone=phone
        self.count=count

        dial=MessageDialog(None,"处理完成！请保存~")
        dial.ShowModal()
       
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
        self.Show(True)        #显示框架  

    def OnQuit(self, e):    #自定义函数　响应菜单项　　  
        self.Close()


    def get_write_path(self,event):
        dlg = DirDialog(self,u"选择文件夹",style=DD_DEFAULT_STYLE)  
        # print("2:",self.phone)
        if dlg.ShowModal() == ID_OK:  
            Topath=dlg.GetPath()
            Topath=str(Topath)
            # print(Topath)
            try:
                # print('1')
                Excel_file = xlwt.Workbook() 
                sheet = Excel_file.add_sheet('sheet0')
                # print('2')    
                sheet.write(0,0,'phone') 
                sheet.write(0,1,'count') 
                for i in range(len(self.phone)): #这段代码是通用
                        print(i)
                        sheet.write(i+1,0,self.phone[i])
                        sheet.write(i+1,1,self.count[i])
                # print("hello")
                excel_name=Topath+'/ouput.xls'
                # print(excel_name)
                Excel_file.save(excel_name)
                dial=MessageDialog(None,"succeed！")
                dial.ShowModal()
 
            except Exception as e:

                dial=MessageDialog(None,"failed!")
                dial.ShowModal()
        dlg.Destroy()

    def getMyPath(self,event):
        global Path #定义全局变量Path，文件夹路径
        dlg = FileDialog(self,u"选择文件",style=DD_DEFAULT_STYLE)  
        if dlg.ShowModal() == ID_OK:  
            Path=dlg.GetPath()
            return Path        
        dlg.Destroy() 
if __name__ == "__main__":
    app = App()    #创建应用的对象
    myframe = MyFrame()    #创建一个自定义出来的窗口
    #myframe.Center()#正中间显示
    myframe.Show()    #这两句一定要在MainLoop开始之前就执行    
    app.MainLoop()