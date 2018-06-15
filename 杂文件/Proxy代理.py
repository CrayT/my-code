#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 18:08:36 2017

@author: xutao
"""
import urllib
import urllib2
enable_proxy=True
proxy_handler=urllib2.ProxyHandler({'http':'http://some-proxy.com:8080'})
null_proxyhandler=urllib2.ProxyHandler({})
if enable_proxy:
    opener=urllib2.build_opener(proxy_handler)
    if opener:
        print "123"
else:
    opener=urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)