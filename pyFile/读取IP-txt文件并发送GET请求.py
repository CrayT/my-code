
import requests
import time
import random
from bs4 import BeautifulSoup
global summ
global num
summ=0
num=1

def get_ip_list():
        headers = {'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Connection': 'keep-alive',
                'Referer': 'https://www.kuaidaili.com'
                }

        #print("正在获取代理列表...")
        global ip_list
        ip_list = []
        #for k in range(1703,1803):
        #url = 'https://www.kuaidaili.com/free/inha/%s/'%(k)
        url='http://dev.kdlapi.com/api/getproxy/?orderid=904112055830446&num=100&b_pcchrome=1&b_pcie=1&b_pcff=1&protocol=2&method=2&an_an=1&an_ha=1&sep=1'
        #print("k:%s"%(k),url)
        html = requests.get(url=url).text
        #print(html)
        soup = BeautifulSoup(html, 'lxml')

        ips=soup.find_all('p')
        for item in ips:
            print(item)
            ip_list.append(item)
    
        time.sleep(2)
        return ip_list

#ip_list=get_ip_list()
#length=len(ip_list)
ip_list=[]
add='/Users/xutao/Downloads/Python/pyFile/100-7.txt'
with open(add) as f:
    for line in f.readlines():
        print(line)
        ip_list.append(line.strip('\n'))


print("iplist:\n",ip_list,len(ip_list))

def ccc(ip_list,m):
    ip_list=ip_list
    def get_random_ip(ip_list):
        #print("正在设置随机代理...")
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        
        proxy_ip = proxy_list[m]
        print(proxy_ip)
        proxies = {'http': proxy_ip}

        return proxies

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
    # print(resp)
    # print(type(resp))
    #print(resp.text)
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
                #i+=1
                ccc(ip_list,i)
                #print("j:%s\n"%(j))
                #return test()
        except Exception as e:
            #print(e)
            i+=1
            test(i)

            #return test()
        
test(1)
