from wx import * 
import oss2
import requests
import os
import threading
import shutil

class MyFrame(Frame):
    url = "https://webapi.123kanfang.com/v2/user/GetAccessTokenByName?authKey=SinyiTW-430829"
    stsUrl = "https://webapi.123kanfang.com/v2/Authorization/AliyunSTS?bucket=" + "" + "&Authorization=" + ""
    bucket_test = "vrhouse-test"
    testEndPoint = "http://oss-cn-shanghai.aliyuncs.com"
    endPoints = {
    "123kanfang":"http://oss-cn-shenzhen.aliyuncs.com",
    "vrhouse-sixstar":"http://oss-cn-shanghai.aliyuncs.com",
    "123vrbucket":"http://oss-cn-shanghai.aliyuncs.com",
    "offweb3d04":"http://oss-cn-beijing.aliyuncs.com",
    "centanet-123kanfang":"http://oss-cn-beijing.aliyuncs.com",
    "vrhouse":"http://oss-cn-shanghai.aliyuncs.com",
    "sinyi-oss":"http://oss-cn-hongkong.aliyuncs.com",
    "vrhouse-123":"http://oss-cn-shanghai.aliyuncs.com",
    "vrhouse-jp":"http://oss-ap-northeast-1.aliyuncs.com",
    "hkbucket-vr":"http://oss-cn-hongkong.aliyuncs.com"
    }
    def __init__(self):
        Frame.__init__(self,None,-1, title="DataCopy", pos=(300,300),size=(600,350))
        panel = Panel(self,-1)
        self.button1 = Button(panel, -1,"开始拷贝", pos=(420, 25), size=(100,30))
        self.button1.Bind(EVT_BUTTON, self.OnReady)

        StaticText(panel, -1, "V1.0", pos=(520,260))

        StaticText(panel, -1, "请输入ID:", pos = (30,30))
        text_input1 = TextCtrl(panel, -1, style=TE_MULTILINE, pos = (90,25), size = (300,60))
        text_input1.SetEditable(True)
        self.__TextBox1 = text_input1

        StaticText(panel, -1, "当前Bucket:", pos = (30,100))
        text_input2 = TextCtrl(panel, -1,  pos = (100,95), size = (100,30))
        self.__TextBox2 = text_input2

        StaticText(panel, -1, "拷贝进度:", pos=(210, 100))
        self.__progress = StaticText(panel, -1, "0.0%", pos=(270, 100))

        text_output = TextCtrl(panel, -1,style=TE_MULTILINE , pos = (40,130), size = (450,150))
        self.__TextOutBox = text_output

        self.InitUi() 

    def GetDomain(bucket):

        pass

    def GetFileList():

        pass

    def GetToken(self,bucket):
        url = "https://webapi.123kanfang.com/v2/user/GetAccessTokenByName?authKey=SinyiTW-430829"
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
    def CopyData(self, hid, bucket, sts, token):
        Domain = self.endPoints[bucket]
        Auth = oss2.StsAuth(sts["accessKeyId"], sts["accessKeySecret"], sts["securityToken"])
        Bucket = oss2.Bucket(Auth, Domain, bucket)
        
        TestDomain = self.testEndPoint
        TestSts = self.GetSts(token, self.bucket_test)
        TestAuth = oss2.StsAuth(TestSts["accessKeyId"], TestSts["accessKeySecret"], TestSts["securityToken"])
        TestBucket = oss2.Bucket(TestAuth, TestDomain, self.bucket_test)

        prefix = hid + '/'
        abPath = os.getcwd()
        fileCount = 0
        for obj in oss2.ObjectIterator(Bucket, prefix = prefix):
            if obj.key[-1] == '/' or obj.key[-1] == '\\':
                continue
            fileCount += 1
        print('文件数量：', fileCount)

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
        dial=MessageDialog(None,"拷贝完成")
        dial.ShowModal()

    def OnReady(self, event):
        bucket = self.__TextBox2.GetValue()
        hid = self.__TextBox1.GetValue()
        if not bucket or not hid:
            dial=MessageDialog(None,"请输入有效数据")
            dial.ShowModal()
        hids = hid.split('\n')
        print(hids)
        #for id in hids:
        self.OnFire(hids[0], bucket)
    def OnFire(self, hid, bucket):
        token = self.GetToken(bucket)
        sts = self.GetSts(token, bucket)
        threadJob = threading.Thread(target = self.CopyData, args = (hid, bucket, sts, token))
        threadJob.start()
        # threadJob.join()

    def InitUi(self):

        pass

if __name__ == "__main__":
    app = App()   
    myframe = MyFrame()    
    myframe.Show()    
    app.MainLoop()