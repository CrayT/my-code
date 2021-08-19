# encoding: utf-8

from html import unescape
from urllib.parse import urlparse, parse_qs
import subprocess

import telegram
from telegram.error import BadRequest
from telegram.utils.request import Request
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters

import itchat
from itchat.content import *

from urllib.request import urlopen
from bs4 import BeautifulSoup
import  schedule
import _thread
import datetime
import time
# 申请telegram后获得的bot token
TELEGRAM_BOT_TOKEN = "769700212:AAGN02zWIsj4AVQ-p6sxmRZw8zuWtVDnjC4"
CHAT_ID = '728926819'
SUB_SECRET = "wsXT"
# 转发消息的群名, 直接复制就好
GROUP_WHITELIST = []
ALL_GROUP = True
# 要用代理啊，不然连不到telegram服务器啊
HTTP_PROXY = "socks5h://127.0.0.1:1086"


bot_instance = telegram.Bot(token=TELEGRAM_BOT_TOKEN,
                            request=Request(proxy_url=HTTP_PROXY))

update_instance = Updater(bot=bot_instance)


def check_is_myself(msg):
    # friend=itchat.get_friends()
    # print(friend[0])
    # itchat.send_msg("hello",friend[0].UserName)
    if msg.User.UserName == "filehelper":
        return False
    return msg.FromUserName == itchat.originInstance.storageClass.userName


def get_name(msg):
    # print(msg)
    if hasattr(msg.User, "NickName"):
        name = msg.User.NickName
    else:
        name = msg.User.UserName
    print(name)
    return name


@itchat.msg_register([TEXT], isFriendChat=True)
def forward_personal_text(msg):
    global CHAT_ID
    name = get_name(msg)
    if not check_is_myself(msg):
        bot_instance.send_message(CHAT_ID,
                                  "[{name}]({url}) : {content}".format(
                                      name=name,
                                      url="http://google.com?user={}".format(msg["FromUserName"]),
                                      content=msg.Content),
                                  parse_mode="Markdown"
                                  )


@itchat.msg_register(TEXT, isGroupChat=True)
def forward_group_text(msg):
    global CHAT_ID
    if not check_is_myself(msg):
        group_name = unescape(msg.User.NickName)
        if not ALL_GROUP:
            if group_name not in GROUP_WHITELIST:
                return None
        bot_instance.send_message(CHAT_ID,
                                  "[{group}]({url})—[{user}]({url}) : {content}".format(
                                      group=group_name,
                                      url="http://google.com?user={}".format(msg["FromUserName"]),
                                      user=msg.ActualNickName,
                                      content=msg.Content),
                                  parse_mode="Markdown"
                                  )


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True)
def forward_pic(msg):
    global CHAT_ID
    name = get_name(msg)
    if not check_is_myself(msg):
        if hasattr(msg, "IsAt"):
            if not ALL_GROUP:
                if unescape(name) not in GROUP_WHITELIST:
                    return None
            name += "—{}".format(msg.ActualNickName)
        bot_instance.send_message(CHAT_ID,
                                  "[{name}]({url}) sending a {typ}, loading~".format(
                                      name=name,
                                      url="http://google.com?user={}".format(msg["FromUserName"]),
                                      typ=msg["Type"]
                                  ),
                                  parse_mode="Markdown"
                                  )
        # save img
        msg.download(msg['FileName'])
        try:
            bot_instance.send_document(CHAT_ID, document=open('./{}'.format(msg['FileName']), 'rb'))
        except BadRequest:
            pass
        finally:
            subprocess.Popen("rm ./{}".format(msg['FileName']), shell=True)


def sub(bot, update):
    global CHAT_ID
    if update.message.text.split(maxsplit=1)[-1] == SUB_SECRET:
        CHAT_ID = update.message.chat_id
        update.message.reply_text("sub success")


def toggle(bot, update):
    global ALL_GROUP
    ALL_GROUP = not ALL_GROUP
    update.message.reply_text("success, {}".format("receive all" if ALL_GROUP else "filtered"))


def echo(bot, update):
    url = update.message["reply_to_message"]["entities"][0]["url"]
    qs = urlparse(url).query
    target = parse_qs(qs)["user"][0]

    if update.message.text:
        try:
            reply_content = update.message["text"]
            itchat.send_msg(reply_content, target)
        except Exception as e:
            print(e)
    elif update.message.photo:
        new_file = bot.get_file(update.message.photo[-1].file_id)
        print(update.message.photo[-1].file_id)
        new_file.download('tmp.jpg')
        itchat.send_image('tmp.jpg', target)
        subprocess.Popen("rm ./{}".format("tmp.jpg"), shell=True)

def find(bot, update):
    print("hello")
    print(itchat.get_friends())
    name = update.message.text.split(maxsplit=1)[-1]
    print(name)
    flag = False
    for ifriend in itchat.get_friends():
        
        print(ifriend)
        print(ifriend.UserName)
        name_l=[]
        name_l.append(ifriend.UserName)
        name_l.append(ifriend.NickName)
        name_l.append(ifriend.RemarkName)
        print(name_l)
        for item in name_l:
            if name in str(item):
                #friend = itchat.search_friends(name=ifriend.UserName)[0]
                mess = "[{name}](http://google.com?user={url})".format(name=name_l[1],url=name_l[0])
                print(mess)
                bot_instance.send_message(CHAT_ID, mess, parse_mode="Markdown")
                return 

        #         flag = True
        #         break
        #     else:
        #         pass
        # if flag:
        #     break
    
def get_weather():
    resp=urlopen('http://www.weather.com.cn/weather1d/101020300.shtml')
    soup=BeautifulSoup(resp,'html.parser')

    today_weather_day=soup.find_all('p',class_="wea")[0].string
    today_weather_night=soup.find_all('p',class_="wea")[1].string
    today_temperature_high=soup.find_all('p',class_="tem")[0].span.string
    today_temperature_low=soup.find_all('p',class_="tem")[1].span.string
    
    mess="上海宝山区今日天气:\n白天天气: %s\n夜间天气: %s\n最高温度: %s\n最低温度: %s"%(today_weather_day,today_weather_night,today_temperature_high,today_temperature_low)
    
    itchat.send_msg(mess, itchat.originInstance.storageClass.userName) #给自己发信息

def sch(p):
    schedule.every().day.at("08:00").do(get_weather) #定时发送
    while True:
        schedule.run_pending()#确保schedule一直运行
        time.sleep(1)

_thread.start_new_thread( sch, (1,))

dis = update_instance.dispatcher
sub_handler = CommandHandler("sub", sub)
toggle_handler = CommandHandler("t", toggle)
find_handler = CommandHandler("f", find)
message_handler = MessageHandler(Filters.text | Filters.photo, echo)
dis.add_handler(find_handler)
dis.add_handler(sub_handler)
dis.add_handler(toggle_handler)
dis.add_handler(message_handler)

update_instance.start_polling()
itchat.auto_login(hotReload=True)
 
itchat.run(True)
