#coding:utf8
import requests
import json
import time
from xlrd import xldate_as_tuple
from xlrd import open_workbook
import subprocess
import oss2
import os

endPoints = {
    "123kanfang":"http://123kanfang.oss-cn-shenzhen.aliyuncs.com",
    "vrhouse-sixstar":"http://vrhouse-sixstar.oss-cn-shanghai.aliyuncs.com",
    "123vrbucket":"http://123vrbucket.oss-cn-shanghai.aliyuncs.com",
    "offweb3d04":"http://offweb3d04.oss-cn-beijing.aliyuncs.com",
    "centanet-123kanfang":"http://centanet-123kanfang.oss-cn-beijing.aliyuncs.com",
    "vrhouse":"http://vrhouse.oss-cn-shanghai.aliyuncs.com",
    "sinyi-oss":"http://sinyi-oss.oss-cn-hongkong.aliyuncs.com",
    "vrhouse-123":"http://vrhouse-123.oss-cn-shanghai.aliyuncs.com",
    "vrhouse-jp":"http://vrhouse-jp.oss-ap-northeast-1.aliyuncs.com",
    "hkbucket-vr":"http://hkbucket-vr.oss-cn-hongkong.aliyuncs.com"
}
# auth = oss2.Auth('<yourAccessKeyId>', '<yourAccessKeySecret>')
# bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', '<yourBucketName>')
# bucket.put_object_from_file('<yourObjectName>', '<yourLocalFile>')

tempToken = "eyJJc3N1ZXIiOiIxMjNLYW5mYW5nIiwiQXVkaWVuY2UiOiI3NGVmM2EyZTgyY2Y0ZmQwOWNhNzYxMjA1YzhkNGUwYyIsIlN1YmplY3QiOiJBUElBdXRoIiwiRXhwaXJlQXQiOiIyMDIxLTA2LTAyVDAxOjQ0OjE3LjI3MTk3MDlaIiwiQ2xhaW1zIjp7fX0=.fyk1T0iGlx_iqkWQvXlSDQ"


j = 1
k = 1


def mergeProcessData(processData_backup, processData, hid):
    
    floorsB = processData_backup["Floors"]
    roomsB = []
    for floorB in floorsB:
        roomsB += floorB["Rooms"]
        # print(floorB.keys())
        if "InActiveRooms" in floorB.keys() and len(floorB["InActiveRooms"]) != 0:
            roomsB += floorB["InActiveRooms"]
    panoB = []
    for roomB in roomsB:
        for pano in roomB["PanoramaImages"]:
            panoB.append(pano)



    floors = processData["Floors"]
    rooms = []
    for floor in floors:
        rooms += floor["Rooms"]
        # print(floor.keys())
        if "InActiveRooms" in floor.keys() and len(floor["InActiveRooms"]) != 0:
            rooms += floor["InActiveRooms"]
    panos = []
    for room in rooms:
        for pano in room["PanoramaImages"]:
            panos.append(pano)


    #print("backup房间个数:", len(panoB), "processData房间个数:", len(panos))

    if len(panoB) == len(panos): 
        return True
    else:
        #写入hid：
        appendToTxt(hid, len(panoB), len(panos))
        return False

def appendToErrorTxt(hid, e):
    print("处理出错hid", hid)
    with open(u'./errorHid.txt','a+') as f:
        f.write( hid )
        if e:
            f.write("," + str(e))
        f.write("\n")


def appendToTxt(hid, l1, l2):
    print("检测到有问题" , hid )
    with open(u'./detectedHid.txt','a+') as f:
        f.write( hid + "," + str(l1) + "," + str(l2) +'\n')


rawdata1 = open_workbook('./0531.xls')
rawdata = rawdata1.sheet_by_index(0)
num = rawdata.nrows #行数

time_start_total = time.time()

def process():
    i = 1
    for row in range(1, num):  #限制从第几行开始读取数据
        print(i)
        i += 1

        time_start = time.time()
        hid = rawdata.row_values(row)[0]
        #print("hid:", hid)

        bucket = rawdata.row_values(row)[1]
        #print("bucket:", bucket)

        bucket = bucket
        # url = "https://webapi.123kanfang.com/v2/Authorization/AliyunSTS?bucket=" + bucket + "&Authorization=" + tempToken
        # response = requests.get(url).json()

        # if response["state"] == 200:

        # ID = response["payload"]["accessKeyId"]
        # key = response["payload"]["accessKeySecret"]
        # stsToken = response["payload"]["securityToken"]

        domain = endPoints[bucket]
        #print("domain:\n", domain)

        # auth = oss2.Auth(ID, key)
        # bucket = oss2.Bucket(auth, domain, bucket)

        processBUrl = domain + "/" + hid +  "/ProcessData_backup.txt"
        processUrl = domain + "/" + hid +  "/ProcessData.txt"

        try:
            try:
                r1 = requests.get(processBUrl)
                r1.encoding='utf-8'
                processB = r1.json()
            except:
                raise Exception("未加载到backup")
            try:
                r2 = requests.get(processUrl)
                r2.encoding='utf-8'
                process = r2.json()
            except:
                raise Exception('加载processData出错')

            mergeProcessData(processB, process, hid)
        except Exception as e:
            print('error:\n', e.args[0])
            appendToErrorTxt(hid, e.args[0])

        time_end = time.time()
        #print('本次耗时：\n', time_end - time_start)

process()


time_end_total = time.time()
print('总耗时：\n', time_end_total - time_start_total)