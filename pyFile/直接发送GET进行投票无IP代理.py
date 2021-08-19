#coding:utf8
'''
读取excel中的号码，进入魏老师的网站模拟操作获取数据，将数据写入excel
'''
import requests
import time
from bs4 import BeautifulSoup
import json
url=u'https://mp.weixin.qq.com/s/ZCTByiRpTpm_q7_ZwxwW6g'
from splinter import Browser

#executable_path = {'/Applications/chrome'}

global summ
global num
summ=0
num=0

# for i in range(1,10):
#     browser = Browser('chrome') #打开谷歌浏览器
#     browser.visit(url)
for i in range(10): 
  
        #time.sleep(2)
        headers={
        "Accept-Encoding": "gzip, deflate",
        "Cache-Control": "max-age=0",
        "Pragma": "no-cache",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Connection": "keep-alive",
        "Host": "www.topsunshine.cn",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "http://www.topsunshine.cn/info/13.html",
        "User-Agent": "User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36"    
        }
        html = requests.get(url=url).text
        print(html)
        time.sleep(3)



'''  
for i in range(len(datavalue)): #这段代码是通用
    #print(len(datavalue[i]))
    #for j in range(len(datavalue[i])):
        c=datavalue[i]
        d=dic_tmp[str(datavalue[i])]
        sheet.write(i,0,c)
        sheet.write(i,1,d)
        #1：正常在用； 2：停机； 3：在网但不可用; 4：不在网; 9：无法查询; -1：手机号码不存在 null：数据不存在 
        if d=='1':
            sheet.write(i,2,'正常在用')
        elif d=='2':
            sheet.write(i,2,'停机')
        elif d=='3':
            sheet.write(i,2,'在网但不可用')
        elif d=='4':
            sheet.write(i,2,'不在网')
        elif d=='9':
            sheet.write(i,2,'无法查询')
        elif d=='-1':
            sheet.write(i,2,'手机号码不存在')
        elif d=='None':
            sheet.write(i,2,'数据不存在')


Excel_file.save('/Users/xutao/Desktop/test_output.xls')
'''