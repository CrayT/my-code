#--coding:utf8-
import requests
import itchat
import time
import csv
import datetime
import pandas as pd
import numpy as np
import threading
KEY = '8edce3ce905a4c1dbb965e6b35c3834d'
address='/home/xutao/Downloads/'
threads=[]
def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        r = requests.post(apiUrl, data=data).json()
        return r.get('text')
    except:
        return 1
white_list = {     
     '1':'@@fa9d8c74ab8dd22eb217a97d10f21db8ade7b99f52c50754349b5ddb1fabd387',     
     '2':'@e5e897fbea495324fe7bc3991f7eb89d',
    # '3':'@@8f1cb16d09c1316e38026c4d814a9208aaf041c9eceffb3cb594222e85035568',
}

@itchat.msg_register(itchat.content.TEXT)
def mes_reply():
  while(1):
    try:
      MES=[]
      MES=raw_input()
      i=int(MES[0])
      s=MES[2:]
      itchat.send("%s"%(s.decode('utf-8')),mes_list[i])
    except:
      print "error"
mes_list=[]
t = threading.Thread(target=mes_reply)
t.setDaemon(True)
t.start()
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    #print msg
    if (msg['FromUserName'] not in mes_list) :
        mes_list.append(msg['FromUserName'])
    print mes_list.index(msg['FromUserName']),msg['User']['NickName'].encode('utf-8'),msg['User']['RemarkName'].encode('utf-8'),msg['Content'].encode('utf-8')
            #if msg['FromUserName'] in white_list.values():  
            #defaultReply = 'I received: ' + msg['Text']
    #defaultReply="[自动回复]学习中，稍等～".decode('utf-8')
    row=[str(msg['User']['NickName'].encode('utf-8')),str(msg['Content'].encode('utf-8')),str(msg['User']['City'].encode('utf-8')),str(msg['User']['Sex']),str(msg['User']['KeyWord'].encode('utf-8')),str(msg['User']['PYQuanPin'].encode('utf-8')),str(msg['User']['Signature'].encode('utf-8')),str(datetime.datetime.fromtimestamp(msg['CreateTime']))]
    out=open("/home/xutao/Downloads/chat_record.csv","a+")
    csv_writer=csv.writer(out,dialect="excel")
    csv_writer.writerow(row)
    
    #reply = get_response(msg['Text'])
            #return reply or defaultReply
    #return reply or defaultReply
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def text_reply(msg):
    #print msg
    if (msg['User']['UserName'] not in mes_list) :
            mes_list.append(msg['User']['UserName'])

    row=[str(msg['User']['NickName'].encode('utf-8')),str(msg['Content'].encode('utf-8')),str(msg['User']['City'].encode('utf-8')),str(msg['User']['Sex']),str(msg['User']['KeyWord'].encode('utf-8')),str(msg['User']['PYQuanPin'].encode('utf-8')),str(msg['User']['Signature'].encode('utf-8')),str(datetime.datetime.fromtimestamp(msg['CreateTime'])),str(msg['ActualNickName'].encode('utf-8'))]
    out=open("/home/xutao/Downloads/chat_record.csv","a+")
    csv_writer=csv.writer(out,dialect="excel")
    csv_writer.writerow(row)
    print  mes_list.index(msg['User']['UserName']),msg['User']['NickName'].encode('utf-8'),msg['ActualNickName'].encode('utf-8'),msg['User']['RemarkName'].encode('utf-8'),msg['Content'].encode('utf-8')
            #if msg['FromUserName'] in white_list.values():  
            #defaultReply = 'I received: ' + msg['Text']
    #defaultReply="[自动回复]学习中，稍等～".decode('utf-8')
    defaultReply = 'OK！' .decode('utf-8')
    #reply = get_response(msg['Text'])
            #return reply or defaultReply
    #return reply or defaultReply
@itchat.msg_register([itchat.content.PICTURE,itchat.content.RECORDING,itchat.content.ATTACHMENT,itchat.content.VIDEO],isGroupChat=True)
def download_files(msg):
        #print msg
        print msg['Text']
        msg['Text']('/home/xutao/Downloads/wechat_dow_pic/'+msg['FileName'])
@itchat.msg_register([itchat.content.PICTURE,itchat.content.RECORDING,itchat.content.ATTACHMENT,itchat.content.VIDEO])
def download_file(msg):
        print msg['Text']
        msg['Text']('/home/xutao/Downloads/wechat_dow_pic/'+msg['FileName'])
itchat.auto_login(hotReload=True)
itchat.run()