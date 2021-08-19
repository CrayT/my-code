import requests
import json
from urllib.request import urlretrieve

url=u"http://47.103.131.230:5010/api/FloorPlan/GenerateFloorPlan2D"

headers = {
        "Host": "youpin.mi.com",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://youpin.mi.com/", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
}

hid_list=[]
txtPath=u'C:/Users/XT/Desktop/hidList.txt'
with open(txtPath) as f:
    for line in f.readlines():
        print(line)
        hid_list.append(line.strip('\n'))
print("房源列表:\n",hid_list,len(hid_list))


def download(imgUrl, name, hid):
    print("开始下载：" + name)
    r = requests.get(imgUrl)
    with open('./image/' + hid + "_" + name, 'wb') as f:
        f.write(r.content)    

for hid in hid_list:
    data={
    "packageId" : hid,
    "bucket" : "vrhouse-test",
    "styles" : "anjuke",
    "viewStyle":''
    }
    r = requests.post(url, data=data,  headers=headers)
    res = r.json()
    print("请求结果：\n", res)
    if len(res['payload']) > 0:
        for item in res['payload']:
            floorPlanUrl = item['floorPlanUrl']
            export = item['exportUrl']
            cover = item['coverUrl']
            jiangfang = item['jiangfangUrl']
            if floorPlanUrl:
                name = floorPlanUrl.split("/")[-1]
                download("http:" + floorPlanUrl, name, hid )

            if export:
                name = export.split("/")[-1]
                download("http:" + export, name, hid )

            if cover:
                name = cover.split("/")[-1]
                download("http:" + cover, name, hid )
            
            if jiangfang:
                name = jiangfang.split("/")[-1]
                download("http:" + jiangfang, name, hid)


    
