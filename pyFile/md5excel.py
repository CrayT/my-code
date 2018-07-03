#coding:utf8
from openpyxl import load_workbook
from xlrd import open_workbook
from  xlwt import Workbook
from wx import * 
import hashlib
class MyFrame(Frame):
    Path=''
    global datavalue 
    datavalue=[]
    def __init__(self):
        Frame.__init__(self,None,-1,title="Excel加密处理",pos=(300,300),size=(300,300))
        panel=Panel(self,-1)
        self.button1=Button(panel,-1,"打开Excel",pos=(100,50),size=(100,40))
        self.button2=Button(panel,-1,"开始处理",pos=(100,150),size=(100,40))
        self.button1.Bind(EVT_BUTTON,self.getMyPath)
        self.button2.Bind(EVT_BUTTON,self.run_file)
        StaticText(panel,-1,"2018-7",pos=(220,220))
        self.InitUI() 
    def getMyPath(self,event):
        dlg = FileDialog(self,u"选择文件",style=DD_DEFAULT_STYLE)  
        if dlg.ShowModal() == ID_OK:  
            MyFrame.Path=dlg.GetPath()     
        dlg.Destroy() 

    def run_file(self,event):  #输出识别号码
        try:
            path=MyFrame.Path
            rawdata1=open_workbook(path)
            rawdata=rawdata1.sheet_by_index(0)
            num=rawdata.nrows #行数
            for row in range(0,num):  #限制从第几行开始读取数据
                rdata=rawdata.row_values(row)  
                datavalue.append(rdata)
        
            Excel_file = Workbook() 
            sheet = Excel_file.add_sheet('sheet0')
            for i in range(len(datavalue)): 
                for j in range(len(datavalue[i])):
                    if j==1 and i!=0:
                        if len(str(datavalue[i][j]))==18:
                            m2 = hashlib.md5()   
                            m2.update(str(datavalue[i][j]).encode('utf-8'))   
                            c=m2.hexdigest()
                        else:
                            dial=MessageDialog(None,"文件第二列不是18位身份证号码，请确认！")
                            dial.ShowModal() 
                            exit()
                    else:
                        c=datavalue[i][j]
                    sheet.write(i,j,c)  
            Topath=str(path).split('.')[0]
            fileName=Topath+str('-md5')
            form=str(path).split('\\')[-1].split('.')[-1]
            pathname=str(fileName)+'.'+str(form)
            Excel_file.save(str(pathname))
            dial=MessageDialog(None,"加密身份信息完成！已自动保存到原路径。")
            dial.ShowModal()  
        except:
            dial=MessageDialog(None,"处理出错，请确认文件格式！")
            dial.ShowModal()  

    def InitUI(self):    #自定义的函数,完成菜单的设置  
        menubar = MenuBar()        #生成菜单栏  
        filemenu = Menu()        #生成一个菜单  
        qmi1 = MenuItem(filemenu,1, "help")     #生成一个help菜单项  
        qmi2 = MenuItem(filemenu,2, "Quit")  #quit项，id设为2，在bind中调用
        filemenu.Append(qmi1)            #把菜单项加入到菜单中  
        filemenu.Append(qmi2)  
        menubar.Append(filemenu, "&File")        #把菜单加入到菜单栏中  
        self.SetMenuBar(menubar)            #把菜单栏加入到Frame框架中  
        self.Bind(EVT_MENU, self.OnQuit, id=2)    #给菜单项加入事件处理，id=2  
        self.Bind(EVT_MENU, self.help_window, id=1)  #help窗口
        self.Show(True)        #显示框架  
    def OnQuit(self, e):    #自定义函数　响应菜单项　　  
        self.Close()
    def help_window(self,event): #定义help窗口
        dial=MessageDialog(None,"注意格式统一！",pos=(10,10)) #测试用
        dial.ShowModal()

if __name__ == "__main__":
    app = App()    #创建应用的对象
    myframe = MyFrame()    #创建一个自定义出来的窗口
    myframe.Show()    #这两句一定要在MainLoop开始之前就执行    
    app.MainLoop()