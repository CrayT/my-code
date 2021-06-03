from wx import * 
import oss2
import requests
import os
import threading
import shutil
from multiprocessing import Process
import pymysql
import json
class MyFrame(Frame):
    url = "https://webapi.123kanfang.com/v2/user/GetAccessTokenByName?authKey=SinyiTW-430829"
    stsUrl = "https://webapi.123kanfang.com/v2/Authorization/AliyunSTS?bucket=" + "" + "&Authorization=" + ""
    bucket_test = "vrhouse-test"
    testEndPoint = "http://oss-cn-shanghai.aliyuncs.com"
    Default_EndPoint = "http://oss-cn-shanghai.aliyuncs.com"
    
    
    def __init__(self):
        Frame.__init__(self,None,-1, title="DataCopy", pos=(300,300),size=(600,350))
        panel = Panel(self,-1)
        self.button1 = Button(panel, -1,"开始拷贝", pos=(420, 25), size=(100,30))
        self.button1.Bind(EVT_BUTTON, self.OnReady)

        StaticText(panel, -1, "V1.0", pos=(520,260))

        StaticText(panel, -1, "请输入IDs:\n(多个换行)", pos = (30,30))
        text_input1 = TextCtrl(panel, -1, style=TE_MULTILINE, pos = (90,25), size = (300,60))
        text_input1.SetEditable(True)
        self.__TextBox1 = text_input1

        #StaticText(panel, -1, "当前Bucket:", pos = (30,100))
        #text_input2 = TextCtrl(panel, -1,  pos = (100,95), size = (100,30))
        #self.__TextBox2 = text_input2

        #当前处理第几个
        self.__progressNumber = StaticText(panel, -1, "", pos=(220, 100))

        StaticText(panel, -1, "拷贝进度:", pos=(50, 100))
        self.__progress = StaticText(panel, -1, "0.0%", pos=(110, 100))

        text_output = TextCtrl(panel, -1,style=TE_MULTILINE , pos = (40,130), size = (450,150))
        self.__TextOutBox = text_output

        self.InitUi() 
        self.ConnectDB()
            
    def GetToken(self, hid):
        url = "https://webapi.123kanfang.com/v2/user/GetAccessTokenByName?authKey="+ hid
        res = requests.get(url).json()
        if res["state"] == 200:
            return res["payload"]["token"]
        return ""

    def GetSts(self, token, bucket):
        stsUrl = "https://webapi.123kanfang.com/v2/Authorization/AliyunSTS?bucket=" + bucket + "&Authorization=" + token
        res = requests.get(stsUrl).json()
        print('sts:\n', res)
        if res["state"] == 200:
            return res["payload"]
        return ""
    
    def CopyData(self, i, length, hid, bucket, sts, token):
        print('参数：\n',i, length, hid, bucket, sts, token)
        
        Domain = self.GetDomain(bucket)
        print('endpoint:\n', Domain)
        Auth = oss2.StsAuth(sts["accessKeyId"], sts["accessKeySecret"], sts["securityToken"])
        Bucket = oss2.Bucket(Auth, Domain, bucket)
        
        TestDomain = self.testEndPoint
        testToken = self.GetToken("SinyiTW-430829")
        TestSts = self.GetSts(testToken, self.bucket_test)
        TestAuth = oss2.StsAuth(TestSts["accessKeyId"], TestSts["accessKeySecret"], TestSts["securityToken"])
        TestBucket = oss2.Bucket(TestAuth, TestDomain, self.bucket_test)

        prefix = hid + '/'
        abPath = os.getcwd()
        print(Bucket, prefix)
        fileCount = 0
        try:
            for obj in oss2.ObjectIterator(Bucket, prefix = prefix):
                if obj.key[-1] == '/' or obj.key[-1] == '\\':
                    continue
                fileCount += 1
            if fileCount == 0:
                print("空文件，结束")
                return
        except Exception as e:
            print('无权限',e)
            dial=MessageDialog(None,"当前hid无权拷贝！" + hid)
            dial.ShowModal()
            return
        print('文件数量：', fileCount)
        self.__progressNumber.SetLabel('当前拷贝第' + str(i + 1) + "/" + str(length) + "个")
        currCopy = 0
        for obj in oss2.ObjectIterator(Bucket, prefix = prefix):
            subPath = obj.key
            if subPath[-1] == '/' or subPath[-1] == '\\':
                continue
            #print('file: ', subPath)
            subPath.replace("/", "\\")
            
            subPath = os.path.dirname(subPath)
            subPath.replace("/", "\\")
            self.__TextOutBox.AppendText(obj.key +"\n")

            hidPath = abPath + "\\" + subPath
            hidPath = hidPath.rstrip("\\")

            if not os.path.exists(hidPath):
                os.makedirs(hidPath)

            Bucket.get_object_to_file(obj.key, './' + obj.key)

            TestBucket.put_object_from_file(obj.key, './' + obj.key)
            os.remove('./' + obj.key)
            currCopy += 1
            progress = str(format(((currCopy / fileCount) * 100), '.1f')) + "%"
            self.__progress.SetLabel(progress)

        shutil.rmtree(abPath + "/" + hid)


    def OnReady(self, event):
        #bucket = self.__TextBox2.GetValue()
        hid = self.__TextBox1.GetValue()
        if not hid:
            dial=MessageDialog(None,"请输入Hid")
            dial.ShowModal()
            return
        hids = hid.split('\n')
        print(hids)
        
        threadJob = threading.Thread(target = self.Start, args = (hids,))
        threadJob.start()
    
    def OnFire(self, i, length, hid, bucket):
        prefix = hid.split("_")[0]
        token = self.GetToken(prefix)
        sts = self.GetSts(token, bucket)
        self.CopyData(i, length,  hid, bucket, sts, token)
        
    def Start(self, hids):
        for i in range(len(hids)):
            id = hids[i]
            bucket = self.GetBucket(id)
            self.OnFire(i, len(hids), id, bucket)
        dial=MessageDialog(None,"拷贝完成")
        dial.ShowModal()

    def GetBucket(self, hid):
        print(hid)
        sql = """select Bucket from housetask where PackageId=\"%s\""""%(str(hid))
        print(sql)
        try:
            self.cursor.execute(sql)  
            res = self.cursor.fetchall()
            print('数据库查询结果：', res[0][0])
            bucket = res[0][0]
            return bucket

        except Exception as e:
            print("数据库查询error", e)
            self.cursor.rollback()
        self.cursor.close()
    def GetDomain(self, bucket):
        sql = """select config from packageaccessconfig where `key`=\"%s\""""%(str(bucket))
        print(sql)
        try:
            self.cursor.execute(sql)  
            res = self.cursor.fetchall()
            print('数据库查询结果：', res[0][0])
            res = json.loads(res[0][0])
            endpoint  = res["EndPoint"]
            return "http://" + endpoint

        except Exception as e:
            print("数据库查询error", e)
            self.cursor.rollback()
            dial=MessageDialog(None,"数据库查询错误" + str(bucket))
            dial.ShowModal()
        self.cursor.close()

    def InitUi(self):

        pass
    def ConnectDB(self):
        self.db = pymysql.connect(host="101.132.5.85", user="donghao", password="123456", database="vr_cloud_customer" , charset='utf8') #mysql数据库
        self.cursor = self.db.cursor()

if __name__ == "__main__":
    app = App()   
    myframe = MyFrame()    
    myframe.Show()    
    app.MainLoop()