#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 08:51:29 2017

@author: xutao
"""

import urllib2
import cookielib
import urllib
filename='cookie.txt'
cookie=cookielib.MozillaCookieJar(filename)
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#查看淘宝登陆页，找到用户名和密码的name。
#postdata=urllib.urlencode({'phone_num':'18801737807','password':'wsxt1225','_xsrf':'64373930383738362d633137322d346532322d386561322d326630343137376563383933'})
#以下是登录页网址
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/52.0.2743.116 Safari/537.36',
    'Referer':'https://www.zhihu.com/'
}
value = {'password':'wsxt1225',
    'remember_me':'True',
    'phone_num':'18801737807',
    '_xsrf':'64373930383738362d633137322d346532322d386561322d326630343137376563383933'
}
loginUrl='https://www.zhihu.com/#signin'
#模拟登陆
data=urllib.urlencode(value)
#初始化一个CookieJar来处理Cookie
cookieJar=cookielib.CookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cookieJar)
#实例化一个全局opener
opener=urllib2.build_opener(cookie_support)
request = urllib2.Request(loginUrl, data, headers)
result=opener.open(request)
print result.read()

