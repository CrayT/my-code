#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 21:43:21 2017

@author: xutao
"""
import re
import requests
import random
import urllib2
import urllib
class download:
    def __init__(self):
        self.iplist=[]
        #IP代理网站，这个已经挂了，需要再另找一个，作为示例
        html="http://www.xicidaili.com"
        user_agent='Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers={'User-Agent':user_agent}
        request=urllib2.Request(html,headers=headers)
        response=urllib2.urlopen(request)
        result=response.read()
#啊洗吧，为了提取出IP和端口，真费了好大劲写这个正则式！！。。。。
        pattern=re.compile('alt="Cn" /></td>.*?<td>(\d\d.*?)</td>.*?<td>(\d\d.*?)</td>',re.S)
        iplistn=re.findall(pattern,result)
        for ip in iplistn:
            IP=ip[0]+':'+ip[1]
            self.iplist.append(IP)  #添加进iplist
        self.user_agent_list=[         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]
        def get(self,url,proxy=None,num_retries=6):
            print "开始获取",url
            UA=random.choice(self.user_agent_list)
            headers={'User-Agent':UA}
            if proxy==None: #代理为空时，不需要代理
                try:
                    response=requests.get(url,headers=headers,timeout=timeout)
                    return response
                except:
                    if num_retries>0:
                        time.sleep(10) #延迟10秒
                        print"获取网页出错，10S后获取倒数第:",num_retries,"次"
                        return self.get(url,timeout,num_retries-1) #调用自身，并次数减一
                    else:
                        print "开始使用代理"
                        time.sleep(10)
                        IP=''.join(str(random.choice(self.iplist)).strip())
                        proxy={'http':IP}
                        return self.get(url,timeout,proxy)
            else: #代理不空
                try:
                    IP=''.join(str(random.choice(self.iplist)).strip())
                    proxy={'http':IP}  #构造一个代理
                #使用代理获取response
                except:
                    if num_tries>0:
                        time.sleep(10)
                        IP=''.join(str(random.choice(self.iplist)).strip())
                        proxy={'http':IP}
                        print "正在更换代理，10S后重新获取倒数第",num_tries,"次"
                        print "当前代理是：",proxy
                        return self.get(url,timeout,num_retries-1)
                    else:
                        print "代理不好使，取消代理！"
                        return self.get(url,3)
       
        


