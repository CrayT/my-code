#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 11:59:05 2017

@author: xutao
"""
import urllib
import urllib2
import re
class BDTB:
    def __init__(self,baseUrl,seeLZ):
        self.baseURL=baseUrl
        self.seeLZ='?see_lz='+str(seeLZ)
        self.tool=Tool()
    def getPage(self,pageNum):
        try:
            url=self.baseURL+self.seeLZ+'&pn='+str(pageNum)
            request=urllib2.Request(url)
            response=urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print e.reason
                return None
    def getContent(self,page):
    #下面一行正则中，加括号代表要匹配括号内的字符串
        pattern=re.compile('<div id="post_content.*?>(.*?)</div',re.S)
        items=re.findall(pattern,page)
        f=1  #楼层从1开始
        for item in items:
            print f," 楼:"
            print self.tool.Replace(item)
            print '\n'
            f+=1 
#获取页面数：
    def getPageNum(self,page):
      #  page=self.getPage(1)
        pattern=re.compile('<li class="l_reply_num.*?max-page="(\d)"',re.S)
        result=re.search(pattern,page)
        if result:
            return result.group(1)  #group表示匹配到的第一个括号内的字符串
        else:
            return None
class Tool:
    #去除图片链接
    removeImg=re.compile('img.*?>',re.S)
    #去除<br>换行符
    removeBR=re.compile('<br><br>|<br>',re.S)  #写两个以上的<br>换行符全部替换掉一个
    #替换文中的<a...</a>
    removeBD=re.compile('<a href.*?/a>',re.S)
    #替换文中的 <
    removeHH=re.compile('<',re.S)
    def Replace(self,ITEM):
        ITEM=re.sub(self.removeImg,' ',ITEM)
        ITEM=re.sub(self.removeBR,'\n',ITEM)
        ITEM=re.sub(self.removeBD,' ',ITEM)
        ITEM=re.sub(self.removeHH,' ',ITEM)
        return ITEM
baseURL='http://tieba.baidu.com/p/3138733512'
bdtb=BDTB(baseURL,1)
#bdtb.getPageNum(bdtb.getPage(1)) 测试获取页面数
pageNum=bdtb.getPageNum(bdtb.getPage(1))
p=1  #先获取第一页
while(p<=int(pageNum)):   #pageNum为字符串类型，若不加int转换，则循环无法停止。。
    print "第",p,"页:\n"
    bdtb.getContent(bdtb.getPage(p))
    p+=1
        