#coding:utf8
'''
读取excel中的号码，进入魏老师的网站模拟操作获取数据，将数据写入excel
'''
import requests
import time
import json
url=u'http://iic2.shu.edu.cn/shuzi/SZ002Test.aspx'
from splinter import Browser
from xlrd import xldate_as_tuple
from openpyxl import load_workbook
from xlrd import open_workbook
import  xlwt
#executable_path = {'/Applications/chrome'}
rawdata1=open_workbook('/Users/xutao/Desktop/04.xlsx')
rawdata=rawdata1.sheet_by_index(0)
datavalue=[]
num=rawdata.nrows #行数
for row in range(0,num):  #限制从第几行开始读取数据
    #print(rawdata.row_values(row))
    rdata=rawdata.row_values(row)  
    
    datavalue.append(str(int(rdata[0])))
#print(datavalue)
#ret_value=[]
dic_tmp={}
i=1
for item in datavalue:
    browser = Browser('chrome') #打开谷歌浏览器
    browser.visit(url)
    browser.find_by_id('txtMobile').fill(str(item))
    time.sleep(0.1)
    browser.find_by_id('txtPrivate_key').fill('f2d68d31-7566-48d8-8ac0-c26b76e9a1a6')
    time.sleep(0.1)
    browser.find_by_id('btnURL2').click()
    time.sleep(0.2)
    browser.find_by_id('btnSubmit').click()
    time.sleep(0.2)
    #r1c1=browser.find_by_xpath('//*[@id="form1"]/div[3]/table/tbody/tr[2]/td[2]').first.value
    r1c1=browser.find_by_id('txtReturn').first.value

    dic1=json.loads(r1c1)

    if not dic1['data']:
        print("第",i,'个:',item,'Null')
        dic_tmp[item]='None'
    if  dic1['data']:
        print("第",i,'个:',item,dic1['data'][0]['value'])
        dic_tmp[item]=dic1['data'][0]['value']
    #ret_value.append(dic1['data'][0]['value'])
    browser.quit()
    i+=1



Excel_file = xlwt.Workbook() 
sheet = Excel_file.add_sheet('sheet0')
          
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