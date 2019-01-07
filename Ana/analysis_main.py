#coding:-utf8--
#import ana_function as af #
import ana_function as af #
import pandas as pd
#address="/Users/xutao/Downloads/Python/data_set/phonedata/移动通话详单采集结果1" #MAC 定义文件地址，下面代码会调用。
#address="/home/xutao/Downloads/Python/data_set/phonedata的副本/运营商数据"  #实验室
#af.data_to_csv() #调用写csv函数，调用一次即可。
def print_num():
    import csv
    with open('/Users/xutao/Downloads/Python/data_set/phonedata_zhang/0.csv','rb') as myFile:  
        lines=csv.reader(myFile)  
        for line in lines:  
            #if(line[1]=='18616002411'):
            if(line[11]=='2'):
                print line
rawdata=pd.read_csv('/Users/xutao/Downloads/Python/data_set/phonedata_zhang/0.csv') #MAC
#print_num()
print "len(csv):",len(rawdata)
from sklearn.cross_validation import train_test_split
features=['weekday','start_hour','use_time','call_days'] #选特征
#lable=['relation']
#data_train=rawdata[features]
#data_lable=rawdata[lable]
#print data #测试
#x_train,x_test,y_train,y_test=train_test_split(data_train,data_lable,test_size=0.4,random_state=1)

#KNC预测：
def knc():
    from sklearn.neighbors import KNeighborsClassifier #采用K近邻分类器进行分类
    from sklearn.metrics import classification_report
    KNC=KNeighborsClassifier()
    KNC.fit(x_train,y_train)
    y_predict=KNC.predict(x_test)
#print y_test,y_predict
    lables=[0,1,2]
    target_names=['other','wife','family']
    print'The accuracy of K近邻 is',KNC.score(x_test,y_test)
    print classification_report(y_test,y_predict,target_names=target_names)
    test=[2,23,7,1,55] #自定义特征进行预测测试
    test_p=KNC.predict(test)
    print "您输入的特征预测为:",test_p[0]
    y_test_matrix=y_test.values
#print int(y_test[0:1].relation) #抽出标记，测试用
#print y_test.index[0] #抽出行号 测试用
    print "KNC预测以下号码预测错误:"
    for i in range(len(y_test)):
        if (y_predict[i]!=int(y_test[i:i+1].relation)):
            tmp=y_test.index[i]
            print int(rawdata[tmp:tmp+1].phone_num),",实际为",int(y_test[i:i+1].relation),",预测为:",y_predict[i],",周几:",int(rawdata[tmp:tmp+1].weekday),",几点:",int(rawdata[tmp:tmp+1].start_hour),",多长时间:",int(rawdata[tmp:tmp+1].use_time),
            if(int(rawdata[tmp:tmp+1].init_type)):
                print ",主叫"
            else:
                print ",被叫"
        else:
            pass
#随机森林：
def rfc():
    from sklearn.ensemble import RandomForestClassifier 
    RFC=RandomForestClassifier()
    RFC.fit(x_train,y_train)
    y_predict_rfc=RFC.predict(x_test)
    print "The accuracy of RFC is:",RFC.score(x_test,y_test)
    print classification_report(y_test,y_predict_rfc,target_names=target_names)
    print "RFC预测以下号码预测错误:"
    for i in range(len(y_test)):
        if (y_predict_rfc[i]!=int(y_test[i:i+1].relation)):
            tmp=y_test.index[i]
            print int(rawdata[tmp:tmp+1].phone_num),",实际为",int(y_test[i:i+1].relation),",预测为:",y_predict_rfc[i],",周几:",int(rawdata[tmp:tmp+1].weekday),",几点:",int(rawdata[tmp:tmp+1].start_hour),",多长时间:",int(rawdata[tmp:tmp+1].use_time),
            if(int(rawdata[tmp:tmp+1].init_type)):
                print ",主叫"
            else:
                print ",被叫"
        else:
            pass

#梯度提升：
def gbc():
    from sklearn.ensemble import GradientBoostingClassifier
    GBC=GradientBoostingClassifier()
    GBC.fit(x_train,y_train)
    y_predict_gbc=GBC.predict(x_test)
    print "The accuracy of GBC is:",GBC.score(x_test,y_test)
    print classification_report(y_test,y_predict_gbc,target_names=target_names)
    print "GBC预测以下号码预测错误:"
    for i in range(len(y_test)):
        if (y_predict_gbc[i]!=int(y_test[i:i+1].relation)):
            tmp=y_test.index[i]
            print int(rawdata[tmp:tmp+1].phone_num),",实际为",int(y_test[i:i+1].relation),",预测为:",y_predict_gbc[i],",周几:",int(rawdata[tmp:tmp+1].weekday),",几点:",int(rawdata[tmp:tmp+1].start_hour),",多长时间:",int(rawdata[tmp:tmp+1].use_time),
            if(int(rawdata[tmp:tmp+1].init_type)):
                print ",主叫"
            else:
                print ",被叫"
        else:
            pass