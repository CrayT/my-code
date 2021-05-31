#coding:utf8
'''
读取excel中的号码，进入魏老师的网站模拟操作获取数据，将数据写入excel
'''
import requests
import time
import json
import pandas as pd
from splinter import Browser

from xlrd import xldate_as_tuple
from openpyxl import load_workbook
from xlrd import open_workbook
import  xlwt
import requests
import json

url=u'http://webapi.123kanfang.com/v2/houseTask/FinishHouseTask'
token2 = "eyJJc3N1ZXIiOiIxMjNLYW5mYW5nIiwiQXVkaWVuY2UiOiI0ODZjMzRmMDcwYTE0ZTVlOThmNWFhOTg1NDhlYWEzZiIsIlN1YmplY3QiOiJBUElBdXRoIiwiRXhwaXJlQXQiOiIyMDIwLTEyLTMwVDA3OjUxOjE4LjM1Njg2OTVaIiwiQ2xhaW1zIjp7fX0=.eqyDgX5YYzOTIMXmB1aNPg"
token1="eyJJc3N1ZXIiOiIxMjNLYW5mYW5nIiwiQXVkaWVuY2UiOiI5NjNkMjE3MDgxMmI0ODI0YWRkYjRjMjU0NTA5YTk1NyIsIlN1YmplY3QiOiJBUElBdXRoIiwiRXhwaXJlQXQiOiIyMDIwLTEyLTMwVDA2OjI0OjMyLjA5ODY1OTZaIiwiQ2xhaW1zIjp7fX0=.D5UZmoYH8-BvKxV4wb0p_w"


Hid=[[],[]]

rawdata1=open_workbook('D:\\资料\\test2.xls')

for i in range(2):
    print(i)

    rawdata=rawdata1.sheet_by_index(i)
    datavalue=[]
    flag=True
    num=rawdata.nrows #行数
    for row in range(0, num):  #限制从第几行开始读取数据
        
        hid = rawdata.row_values(row)[0]
        print(hid)
        if i == 0:
            token=token1
        else:
            token=token2

        weburl = "http://webresource.123kanfang.com/31test-403/1228/studioClient4/client.html?v=2020121101&noCache=true&hid=" + hid + "&domain=//vrhouse.oss-cn-shanghai.aliyuncs.com/&token="+ token + "&vconsole=1&clearCache=1607662144149"
        browser = Browser('chrome') #打开谷歌浏览器
        browser.visit(weburl)
        print(weburl)
        time.sleep(5)

        browser.find_by_id('goNextBtn').click()
        data = {
                "packageId": hid,
                "isFinished": "true",
                "Authorization": token1
        }

        time.sleep(5)
        r = requests.post(url, data=data)
        res = json.loads(r.text)
        print(res)
        try:
            if res['state'] == 200:
                print(hid + " 发布成功")
                Hid[0].append(hid)
                browser.quit()

            else:
                print(hid + " 发布失败")
                Hid[1].append(hid)
                browser.quit()
        except:
            Hid[1].append(hid)
            print(hid + "发布失败")

print("执行完毕：\n", Hid)


Excel_file = xlwt.Workbook() 
sheet = Excel_file.add_sheet('sheet0')


for i in range(len(Hid)): #这段代码是通用

        success = Hid[0]
        fail = Hid[1]

        if len(success) > 0:
            for m in range(len(success)):
                hid = str(success[m])
                try:
                    sheet.write(m, 0, hid )
                except:
                    sheet._cell_overwrite_ok = True
                    # do any required operations since we found a duplicate
                    sheet.write(m,  0, hid)
                    sheet._cell_overwrite_ok = False
        else:
            print("全部失败")
        
        if len(fail) > 0:
            for n in range(len(fail)):
                hid = str(fail[n])

                try:
                    sheet.write(n, 1, hid )
                except:
                    sheet._cell_overwrite_ok = True
                    # do any required operations since we found a duplicate
                    sheet.write(n,  0, hid)
                    sheet._cell_overwrite_ok = False
        else:
            print("全部成功")
try:
    Excel_file.save('D:\\资料\\test_output.xls')
     print("已经发布结果写入excel")
except:
    print("发布结果写入excel出错")