
import requests
import time
import random
import urllib.request
from bs4 import BeautifulSoup
global summ
global num
summ=0
num=1
def pro():
        def get_ip_list():
                ip_list=[]
                #api链接，调用API，num字段定义获取数量，dedup=1定义不获取已获取过的IP。
                api_url = "http://dev.kdlapi.com/api/getproxy/?orderid=904112055830446&num=100&dedup=1&sep=1" #&an_ha=1&protocol=1
                req = urllib.request.urlopen(api_url) 
                ipp=req.read().decode('utf-8')
                ip_tmp=ipp.split('\n')
                for item in ip_tmp:
                        ip_list.append(item.strip('\r'))
                return ip_list

        ip_list=get_ip_list()

        print("iplist:\n",ip_list,len(ip_list))

        proxy_list = []
        for ip in ip_list:
                ip_json={}
                ip_json['http']=ip
                ip_json['https']=ip
                proxy_list.append(ip_json)
        def ccc(ip_list,m):
                ip_list=ip_list
                def get_random_ip(ip_list):
                        proxy_ip = proxy_list[m]
                        #proxies = {'http': proxy_ip}
                        return proxy_ip

                urltoupiao = "http://www.topsunshine.cn/toupiao/13.html"


                headers={
                        "Accept-Encoding": "gzip, deflate",
                        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                        "Connection": "keep-alive",
                        "Host": "www.topsunshine.cn",
                        "Upgrade-Insecure-Requests": "1",
                        "Referer": "http://www.topsunshine.cn/index.html",
                        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36",
                        "Cookie": "__cfduid=ddb409282badaa111d2274bf2425ae96a1540785705; Hm_lvt_33211b1c2614f13393ddd3abde21e863=1540785706; Hm_lpvt_33211b1c2614f13393ddd3abde21e863=1540801535"
                }

                time1=random.randint(1,2)
                        
                time.sleep(time1)
                proxy=get_random_ip(ip_list)
                print(proxy)
                resp = requests.get(urltoupiao,headers=headers,proxies=proxy,timeout=15,verify=False) 
                soup = BeautifulSoup(resp.text,'lxml')
                car_list = soup.find('span',{'id':'ContentPlaceHolder2_Label1'})
                print("第%s次尝试结果:\n"%(m),car_list)
                print('\n')
                num+=1
                ss=str(car_list)
                if r"成功" in ss:
                        summ+=1
                        print("\n成功投票：%s次\n"%(summ))
                else:
                        print("成功%s次!\n"%(summ))


                def test(x):
                        for i in range(x,len(ip_list)):   
                                try:
                                        print(str(i))
                                        ccc(ip_list,i)
                                except Exception as e:
                                        i+=1
                                        if i<len(ip_list):
                                                test(i) 
                                        else:
                                                pro()
                test(1)
pro()