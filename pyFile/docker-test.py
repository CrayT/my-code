#coding:utf8
import docker
c=docker.APIClient(base_url='unix://var/run/docker.sock',version='1.21',timeout=10) #version为1.21，最低支持版本
c.start(container='c076737d8aa8') #启动一个容器
c.stop(container='c076737d8aa8')
