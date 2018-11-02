
import requests
import time
import random
from bs4 import BeautifulSoup
global summ
global num
summ=0
num=1

mm=1
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
        for k in range(1,11):
            try:
                #url = 'https://www.kuaidaili.com/free/inha/%s/'%(k)
                
                url='http://www.xicidaili.com/nt/%s'%(k)
                print("k:%s"%(k),url)
                
                html = requests.get(url=url,headers=headers).text
                
                soup = BeautifulSoup(html, 'lxml')

                ips=soup.find(id='ip_list').find_all('tr')

                #print(ips,'\n\nchangdu\n',len(ips))
                

                for i in range(1, len(ips)):
                    ip_info = ips[i]
                    #print(ip_info)
                    ip = ip_info.find_all('td')
                    print(ip[1].text,ip[2].text)
                    ip_list.append(ip[1].text + ':' + ip[2].text)
                #print("代理列表抓取成功.")
                #print(ip_list)
            except:
                continue
            time.sleep(2)
        return ip_list

ip_list=get_ip_list()
length=len(ip_list)

print("iplist:\n",ip_list)

def ccc(ip_list,m):
    ip_list=ip_list
    def get_random_ip(ip_list):
        #print("正在设置随机代理...")
        proxy_list = []
        for ip in ip_list:
            ip_json={}
            ip_json['http']='http://%s'%(ip)
            ip_json['https']='https://%s'%(ip)
            proxy_list.append(ip_json)
        
        proxy_ip = proxy_list[m]
        # print(proxy_ip)
        # proxies = {'http': proxy_ip}
        #print("代理设置成功.")
        print(proxy_ip)
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



    time1=random.randint(3,6)
        
    time.sleep(time1)
    proxy=get_random_ip(ip_list)
    print(proxy)
    #time.sleep(random.randint(1,5))
    resp = requests.get(urltoupiao,headers=headers,proxies=proxy,timeout=15,verify=False) 
    print(resp)
    # print(type(resp))
    soup = BeautifulSoup(resp.text,'lxml')
    car_list = soup.find('span',{'id':'ContentPlaceHolder2_Label1'}).text
    print("\n第%s次尝试结果:\n"%(m),car_list)
    num+=1
    if r"成功" in str(car_list):
        summ+=1
        print("\n成功投票：%s次\n"%(summ))
    else:
        print("成功%s次!\n"%(summ))


def test(x):
    for i in range(x,length):   
        try:
                print(str(i))
                #i+=1
                ccc(ip_list,i)
        except Exception as e:
            i+=1
            test(i)

            #return test()
        
test(1)

