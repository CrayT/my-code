#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 20:44:11 2017

@author: xutao
"""
import requests
import urllib2
import re
import pandas as pd
url_first='https://movie.douban.com/subject/26363254/comments?start=0'
head={'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Mobile Safari/537.36'}
cookies={'cookie':'bid=xMS5vCF4oVg; ap=1; __utma=30149280.726621003.1501925330.1502676772.1504270522.4; __utmb=30149280.0.10.1504270522; __utmc=30149280; __utmz=30149280.1502676772.3.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic'}
#html=requests.get(url_first,headers=head,cookies=cookies)
response=urllib2.urlopen(url_first)
html=response.read()
#print Html
#print html.text #测试代码
reg=re.compile('<a href="(.*?)&amp.*?class="next">') #下一页,提取出字符串：?start=26
ren=re.compile('<span class="votes">(.*?)</span>.*?class="">(.*?)</a>.*?rating" title="(.*?)"></span>.*?<p class="">(.*?)</p>',re.S)
#1:投票，2：评论者，3：评级，4：评论。
zhanlang=re.findall(ren,html)
page=re.findall(reg,html)
P=tuple(page)  #将page转换为字符串
pp=int(re.sub("\D","",P[0]))  #将非数字替换掉，只剩下数字，即页数
start=0
while start<=pp:
    #if"img" in zhanlang:
    #    zhanglang=re.sub(pattern,"",zhanlang)
    #else:
    #    pass
    data=pd.DataFrame(zhanlang)
    #print data
    print "正在写入第",start+1,"页："
    data.to_csv('/Users/xutao/Desktop/zhanlang.csv', header=False,index=False,mode='a+') #写入csv文件,'a+'是追加模式
    url_next='https://movie.douban.com/subject/26363254/comments?start='+str(start)
    start+=1
    response=urllib2.urlopen(url_next)
    html=response.read()
    #如果评论带图片，则下面的正则会连图片链接一起晒出。
    ren=re.compile('<span class="votes">(.*?)</span>.*?class="">(.*?)</a>.*?rating" title="(.*?)"></span>.*?<p class="">(.*?)</p>',re.S)
    zhanlang=re.findall(ren,html)
    i=0
    while i<20:
        #每页20条信息，循环一条条输出。
        print zhanlang[i][0],zhanlang[i][1],zhanlang[i][2],zhanlang[i][3]
        i+=1
    #为什么写到第21页就报错了？？？
print "写入完成！"
#data=[]
#zhanlang=[]
#response=urllib2.urlopen(url_next)
#html=response.read()
#d=pd.read_csv('zhanlang.csv',index_col=0)
#print d
