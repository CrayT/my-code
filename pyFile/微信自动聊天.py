
#coding:utf8
import requests
import itchat
import time
from itchat.content import *
import csv
import datetime
import pandas as pd
import numpy as np
import threading
KEY = '6d4412759d3d4da8ae42fc06a19c144a'
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
        return
white_list = {     
     '1':'@@fa9d8c74ab8dd22eb217a97d10f21db8ade7b99f52c50754349b5ddb1fabd387',     
     '2':'@e5e897fbea495324fe7bc3991f7eb89d',
}
'''
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
      print "123"
mes_list=[]
t = threading.Thread(target=mes_reply)
t.setDaemon(True)
t.start()
'''

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    #print msg
    '''
    if (msg['FromUserName'] not in mes_list) :
        mes_list.append(msg['FromUserName'])
    print mes_list.index(msg['FromUserName']),msg['RecommendInfo']['NickName'].encode('utf-8'),msg['Content'].encode('utf-8')
    '''
    reply = get_response(msg['Text'])
            #return reply or defaultReply
    return reply or defaultReply
'''
@itchat.msg_register(itchat.content.TEXT,isGroupChat=True)
def text_reply(msg):
    #print msg
    if (msg['User']['UserName'] not in mes_list) :
            mes_list.append(msg['User']['UserName'])
    print  mes_list.index(msg['RecommendInfo']['UserName']),msg['Content'].encode('utf-8')
            #if msg['FromUserName'] in white_list.values():  
            #defaultReply = 'I received: ' + msg['Text']
    #defaultReply="[自动回复]学习中，稍等～".decode('utf-8')
    defaultRepshijianly = 'OK！' .decode('utf-8')


    #reply = get_response(msg['Text'])
            #return reply or defaultReply
    #return reply or defaultReply
'''
itchat.auto_login()
itchat.run()