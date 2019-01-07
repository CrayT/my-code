# coding: utf-8
from datetime import datetime
import pandas as pd
import json
import re
import chardet

#号码标准化，同时删除非法数据
def re_phone(phone):
    quhao= ['010', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '0310', '0311', '0312', '0313', 
    '0314', '0315', '0316', '0317', '0318', '0319', '0335', '0349', '0350', '0351', '0352', '0353', '0354', '0355', '0356', 
    '0357', '0358', '0359', '0370', '0371', '0372', '0373', '0374', '0375', '0376', '0377', '0378', '0379', '0391', '0392', 
    '0393', '0394', '0395', '0396', '0398', '0410', '0411', '0412', '0413', '0414', '0415', '0416', '0417', '0418', '0419', 
    '0421', '0427', '0429', '0431', '0432', '0433', '0434', '0435', '0436', '0437', '0438', '0439', '0451', '0452', '0453', 
    '0454', '0455', '0456', '0457', '0458', '0459', '0464', '0467', '0468', '0469', '0470', '0471', '0472', '0473', '0474', 
    '0475', '0476', '0477', '0478', '0479', '0482', '0483', '0510', '0511', '0512', '0513', '0514', '0515', '0516', '0517', 
    '0518', '0519', '0523', '0527', '0530', '0531', '0532', '0533', '0534', '0535', '0536', '0537', '0538', '0539', '0541', 
    '0542', '0543', '0544', '0545', '0546', '0547', '0550', '0551', '0552', '0553', '0554', '0555', '0556', '0557', '0558', 
    '0559', '0561', '0562', '0563', '0564', '0565', '0566', '0571', '0572', '0573', '0574', '0575', '0576', '0577', '0578', 
    '0579', '0580', '0591', '0592', '0593', '0594', '0595', '0596', '0597', '0598', '0599', '0610', '0611', '0612', '0613', 
    '0614', '0615', '0616', '0617', '0618', '0619', '0624', '0730', '0731', '0732', '0733', '0734', '0735', '0736', '0737', 
    '0738', '0739', '0743', '0744', '0745', '0746', '0750', '0751', '0752', '0753', '0754', '0755', '0756', '0757', '0758', 
    '0759', '0760', '0761', '0762', '0763', '0764', '0765', '0766', '0767', '0768', '0769', '0770', '0771', '0771', '0772', 
    '0773', '0774', '0774', '0775', '0775', '0776', '0777', '0778', '0779', '0789', '0790', '0791', '0792', '0793', '0794', 
    '0795', '0796', '0797', '0798', '0799', '0812', '0813', '0816', '0817', '0818', '0825', '0826', '0827', '0830', '0831', 
    '0832', '0832', '0833', '0833', '0834', '0835', '0836', '0838', '0839', '0851', '0852', '0853', '0854', '0855', '0856', 
    '0857', '0858', '0859', '0869', '0870', '0871', '0872', '0873', '0874', '0875', '0876', '0877', '0878', '0879', '0883', 
    '0886', '0887', '0888', '0889', '0890', '0891', '0892', '0893', '0894', '0895', '0896', '0897', '0897', '0898', '0898', 
    '0898', '0898', '0898', '0899', '0899', '0901', '0902', '0903', '0906', '0908', '0909', '0910', '0911', '0912', '0913', 
    '0914', '0915', '0916', '0917', '0919', '0930', '0931', '0932', '0933', '0934', '0935', '0936', '0937', '0937', '0937', 
    '0938', '0939', '0941', '0943', '0951', '0952', '0953', '0954', '0970', '0971', '0972', '0973', '0974', '0975', '0976', 
    '0977', '0990', '0991', '0992', '0993', '0994', '0995', '0996', '0997', '0998', '0999']
    #调整区号
    phone=str(phone).strip()
    if phone.startswith('400'):
        return [phone,'error']
    if phone.startswith('+'):
        phone='0'+phone[1:]
    if phone.startswith('00'):
        phone=phone[1:]
    if phone.startswith('86'):
        phone='0'+phone
    if not phone.startswith('0') and len(phone) in [9,10]:
        phone='0'+phone
    if len(phone)==11 and phone[:1] not in ['0','1']:
        phone='0'+phone
    #截取区号输出
    if not phone.replace('*','0').isdigit():
        return [phone,'error']
    l=len(phone)
    if l==14:
        return [phone,phone[3:]]
    if l==12:
        return [phone,phone[4:]]
    if l==11:
        if phone[:3] in quhao:
            return [phone,phone[3:]]
        elif phone[:4] in quhao:
            return [phone,phone[4:]]
        else:
            return[phone,phone]
    if l==10:
        return [phone,phone[3:]]
    if l==7 or l==8:
        return [phone,phone]
    return [phone,'error']
#日期标准化，返回标准化后的日期或返回error
def re_date(data):
    data=str(data).strip()
    r=re.compile(r'(\d{4}[-/])?\d{1,2}[-/]\d{1,2}\s\d{2}:\d{2}')
    data=re.search(r,data)
    if data==None:
        return 'error'
    year=datetime.now().year  #获取当前年份
    month=datetime.now().month #获取当前月份
    data=data.group().replace('/','-')
    if data.count('-')==1:
        if int(data[0:2])<=month:
            data=str(year)+"-"+data
        else:
            data=str(year-1)+"-"+data
    return data
#主被叫标准化
def re_it(data):
    keys=['被叫','主叫','无条件呼转']
    data=str(data).strip()
    for i in keys:
        if i in data:
            return i
    return 'error'
#通话时长标准化
def re_ut(data):
    data=str(data).strip()
#    if data=="552":
#        return 'error'
    if ':' in data:
        if data.replace(':','0').isdigit():
            return data
    elif '秒' in data:
        data=data.replace('秒','')
        data=data.replace('分',':')
        data=data.replace('时',':')
        return re_ut(data)
    elif data.isdigit():
        data=int(data)
        if data>50000:
            return 'error'
        hour=data//3600
        minute=data%3600//60
        second=data%60
        res=''
        if hour:
            res=str(hour)+':'
        if res!='' or minute!=0:
            res=res+str(minute)+':'
        res=res+str(second)
        return res
    else:
        return 'error'


#探测键名
def find_keys(data,row=0):
    phone_index=[]
    st_index=[]
    it_index=[]
    ut_index=[]
    i_index=None
    p_index=None
    s_index=None
    u_index=None
    for i in data.columns:
        tem=str(data[i][row]).strip()
        if type(tem)==None:
            continue
        if re_date(tem)!='error':
            st_index.append(i)
        elif re_it(tem)!='error':
            it_index.append(i)
        elif re_ut(tem)!='error':
            ut_index.append(i)
        else:
            if tem[0]=='+':
                tem=tem[1:]
            if tem.replace('*','0').isdigit() and len(tem)>5:
                phone_index.append(i)
    if len(phone_index)>1:
        for j in range(row+1,len(data)): 
            for i in phone_index:
                if data[i][j]!=data[i][row]:
                    p_index=i
                    break
            if p_index!=None:
                break
    elif len(phone_index)==1:
        p_index=phone_index[0]
    if len(st_index)>1:
        for j in range(row+1,len(data)):
            for i in st_index:
                if data[i][j]!=data[i][row]:
                    s_index=i
                    break
            if s_index!=None:
                break
    elif len(st_index)==1:
        s_index=st_index[0]
    if len(it_index)>1:
        for j in range(row+1,len(data)):
            for i in it_index:
                if re_it(data[i][j])!='error':
                    i_index=i
                    break
            if i_index!=None:
                break
    elif len(it_index)==1:
        i_index=it_index[0]
    if len(ut_index)>1:
        for j in range(row+1,len(data)):
            for i in ut_index:
                if re_ut(data[i][j])!='error':
                    u_index=i
                    break
            if u_index!=None:
                break
    elif len(ut_index)==1:
        u_index=ut_index[0]
    if p_index==None or s_index==None:
        if row<len(data)-1 and row<20:
            return find_keys(data,row+1)
    if 'use_time' in data.columns:
        u_index='use_time'
    if 'other_cell_phone' in data.columns:
        p_index='other_cell_phone'
    if 'init_type' in data.columns:
        i_index='init_type'
    if 'start_time' in data.columns:
        s_index='start_time'
    return [p_index,s_index,i_index,u_index]
#从json中自动寻找calls列表
def find_calls(info):
    if type(info)==dict:
        for i in info:
            calls=find_calls(info[i])
            if calls!=None:
                return calls
    if type(info)==list:
        if len(info)>0 and type(info[0])==dict:
            for i in info[0]:
                if type(info[0][i])==str and re_it(info[0][i])!='error':
                    return info
        for i in info:
            calls=find_calls(i)
            if calls!=None:
                return calls
    return None  
#将数据转为DataFrame格式后统一解析
def read_df(info):
    ocp_key=''
    st_key=''
    it_key=''
    ut_key=''
    #自动探测可能字段
    auto_key=find_keys(info)
    #print(auto_key)
    if auto_key[0]!=None:
        ocp_key=auto_key[0]
    else:
        return 'error_ocpKeyNotFound'
    if auto_key[1]!=None:
        st_key=auto_key[1]
    else:
        return 'error_stKeyNotFound'
    it_key=auto_key[2]
    ut_key=auto_key[3]
    call_list=[]
    for i in range(len(info)):
        tem={}
        phone=re_phone(info[ocp_key][i])
        st=re_date(info[st_key][i])
        if it_key==None:
            it='error'
        else:
            it=re_it(info[it_key][i])
        if ut_key==None:
            ut='error'
        else:
            ut=re_ut(info[ut_key][i])
        if phone[1]=='error' or st=='error':
            continue
        else:
            tem['phone']=phone
            tem['st']=st
            tem['it']=it
            tem['ut']=ut
            call_list.append(tem)
    return call_list
def read_json(address,encoding):
    info = pd.read_json(address,encoding=encoding)
    calls=find_calls(info.to_dict())
    calls = pd.DataFrame(calls)  
    return read_df(calls)
def read_csv(address,encoding):
    info = pd.read_csv(address,engine='python',encoding=encoding,skip_blank_lines=True,dtype=str)
    return read_df(info)
def read_excel(address,encoding):
    info = pd.read_excel(address,encoding=encoding,skip_blank_lines=True,dtype=str)
    return read_df(info)
#根据文件名读取单个文件
def read_file(path):
    filename=path.split('/')[-1]
    user=filename.split('.')[0]
    ftype=filename.split('.')[1]
    calls=''
    with open(path,'rb') as f:
        encoding=chardet.detect(f.read())['encoding']
    if ftype=='csv':
        calls=read_csv(path,encoding)
    elif ftype=='txt':
        pass
    elif ftype=='json':
        calls=read_json(path,encoding)
    elif ftype=='xls' or ftype=='xlsx':
        calls=read_excel(path,encoding)
    else:
        pass
    data_json={}
    data_json['user']=user
    data_json['calls']=calls
    return data_json
