#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 09:04:23 2017

@author: xutao
"""
import urllib
import urllib2
import sys
import re
class QSBK:
     def __init__(self,page):
         baseUrl='http://www.qiushibaike.com/hot/page/'
         self.url=baseUrl+str(page)
         self.tool=Tool()
#加入headers验证，否则网页内容无法提取
     def getPage(self):         
         user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
         headers={'User-Agent':user_agent}
         try:
             request=urllib2.Request(self.url,headers=headers)
             response=urllib2.urlopen(request)
             return response.read()
         except urllib2.URLError,e:
             if hasattr(e,"code"):
                 print e.code
             if hasattr(e,"reason"):
                 print e.reason
     def getContent(self):
         page=self.getPage()
         pattern=re.compile('<div class="content">.*?<span>(.*?)</span>.*?</div>',re.S)
         result=re.findall(pattern,page)
         #findall返回的是元组，抽取时用[].
         print "按回车获取一个搞笑段子："
         for item in result:
             while True:
                 input=raw_input() #检测是否按下enter键
                 print self.tool.replace(item)  #将item中乱符处理后输出
                 break
             print "你再按一下："  
class Tool:   #替换br换行符 剔除图片链接
    removeBR=re.compile('<br/>')
    removeIMG=re.compile('<img.*?/>')
    #removeHZ=re.compile('<span>[\u4e00-\u9fa5].*?</span>')
    def replace(self,ITEM):
        ITEM=re.sub(self.removeBR,'\n',ITEM)
        ITEM=re.sub(self.removeIMG,'',ITEM)
       # ITEM=re.sub(self.removeHZ,'',ITEM)
        return ITEM
qsbk=QSBK(1)
print "正在链接嗅事百科，请稍等..."
qsbk.getContent()