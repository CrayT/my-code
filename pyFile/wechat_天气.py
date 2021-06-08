# -*- coding:utf-8 -*-
import datetime
import time
import wxpy
from wxpy import *
from urllib.request import urlopen
from bs4 import BeautifulSoup
import  schedule
import itchat
bot=Bot(cache_path=True) #登陆网页微信，并保存登陆状态
def send_message(mess):
    # my_friend = bot.friends()[0] #自己
    # print(my_friend)
    # my_friend.send(mess)
    friend=itchat.get_frients()
    print(friend)
    itchat.send_msg("hello", friend[0]) 

def get_weather():
    resp=urlopen('http://www.weather.com.cn/weather1d/101020300.shtml')
    soup=BeautifulSoup(resp,'html.parser')

    today_weather_day=soup.find_all('p',class_="wea")[0].string
    today_weather_night=soup.find_all('p',class_="wea")[1].string
    today_temperature_high=soup.find_all('p',class_="tem")[0].span.string
    today_temperature_low=soup.find_all('p',class_="tem")[1].span.string
    
    mess="上海宝山区今日天气:\n白天天气: %s\n夜间天气: %s\n最高温度: %s\n最低温度: %s"%(today_weather_day,today_weather_night,today_temperature_high,today_temperature_low)
    
    send_message(mess)

# schedule.every().day.at("13:34").do(get_weather) #定时发送
# while True:
#     schedule.run_pending()#确保schedule一直运行
#     time.sleep(1)
itchat.auto_login(enableCmdQR=True)
get_weather()
itchat.run(True)