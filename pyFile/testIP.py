
import requests
import time
import random
from bs4 import BeautifulSoup
url = 'http://icanhazip.com'

headers = {'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Connection': 'keep-alive',
                'Referer': 'http://icanhazip.com'
                }
proxy={"https":"///27.46.22.243:8888",
       "http":"//27.46.22.243:8888"
}
print(proxy)
# time.sleep(random.randint(1,5))
resp = requests.get(url,headers=headers,proxies=proxy,verify=False) 
# print(resp)
# print(type(resp))
soup = BeautifulSoup(resp.text,'lxml')
print(soup)