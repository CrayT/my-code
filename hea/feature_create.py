#import featuretools as ft
import pandas as pd
import itertools
import math
names=['alloy','num','class','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']

#data=pd.read_csv('/Users/xutao/Nustore Files/我的坚果云/HEA/feature_tools/合并数据集-去除重复.csv',header=0,names=names)
#X1=data[['num','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']]
#X2=data[['num','delta','Hmix','Smix','Fi','RMS','VEC','r','Sc','deltaHmixmax','deltaHmixmin','rootHmix','rootHmix0','rootHmix0+','rootHmix0-']]

#Y=data[["class"]]

def create_features(X1,X2):
    #创建实体
    es = ft.EntitySet(id = 'features')
    #print(X1.sample(5))
    es = es.entity_from_dataframe(entity_id = 'feature1', dataframe = X1, index = 'num',)
    es = es.entity_from_dataframe(entity_id = 'feature2', dataframe = X2, index = 'num',)
    #print("es:\n",es)

    new_relationship = ft.Relationship(es['feature1']['num'],es['feature2']['num'])
    es = es.add_relationship(new_relationship)
    print("es:\n",es)
    #features
    feature_matrix, feature_defs = ft.dfs(entityset=es,target_entity="feature1",max_depth=2)
    print(feature_matrix.iloc[0])

    #print(feature_defs)
    #print(es["feature1"].variables)
    print(type(feature_matrix),feature_matrix.shape)
    return feature_matrix

def generate_feature(X): #根据论文扩充特征
    print(type(X))
    print(X.shape)
    c,r=X.shape
    index_tmp=list(X.columns)
    dim=r
    #第一次对特征本身做扩充
    for m in range(len(index_tmp)):
        list_tmp=X[index_tmp[m]] #每次取出一个特征对应的一列数据。
        list1=[]
        list2=[]
        list3=[]
        list4=[]
        list5=[]
        list6=[]
        for k in range(len(list_tmp)):
            list2.append(pow(abs(list_tmp[k]),1/2)) #根号
            list3.append(pow(list_tmp[k],2)) #平方
            list4.append(pow(list_tmp[k],3)) #三次方
            list5.append(math.log(1+abs(list_tmp[k]))) #log(1+|x|)
            #list6.append(math.exp(list_tmp[k]))
        name2='pow1/2'+str(index_tmp[m])
        name3='pow2'+str(index_tmp[m])
        name4='pow3'+str(index_tmp[m])
        name5='log'+str(index_tmp[m])
        X.insert(dim,"%s"%name2,list2)
        dim=dim+1
        X.insert(dim,"%s"%name3,list3)
        dim=dim+1
        X.insert(dim,"%s"%name4,list4)
        dim=dim+1
        X.insert(dim,"%s"%name5,list5)
        dim=dim+1
    print(X.shape) #407*70

    #第二次扩充：任选三个特征做相乘：
    index_tmp_2=list(X.columns)
    features_3=[]
    for item in itertools.combinations(index_tmp_2,3):
        features_3.append(item)
    print(len(features_3))
    for i in range(len(features_3)):
        a=X[features_3[i][0]] #a\b\c是X中的按feature索引的三列list。
        b=X[features_3[i][1]]
        c=X[features_3[i][2]]
        list1=[]
        list2=[]
        list3=[]
        print("No:",i,'\n')
        for j in range(len(a)):
            #print(a[j],b[j],c[j])
            list1.append(a[j]*b[j]*c[j]) #a*b*c
        name_tmp=str(features_3[i][0])+'+'+str(features_3[i][1])+'+'+str(features_3[i][2])
        X.insert(dim,"%s"%name_tmp,list1)
        dim=dim+1
    print(X.shape)

    #第三次扩充：任选两个特征做相乘：
    features_2=[]
    for item in itertools.combinations(index_tmp_2,2):
        features_2.append(item)
    print(len(features_2))
    for i in range(len(features_2)):
        a=X[features_2[i][0]] #a\b\c是X中的按feature索引的三列list。
        b=X[features_2[i][1]]
        list1=[]
        print("No:",i,'\n')
        for j in range(len(a)):
            #print(a[j],b[j],c[j])
            list1.append(a[j]*b[j]) #a*b*c
        name_tmp=str(features_2[i][0])+'+'+str(features_2[i][1])
        X.insert(dim,"%s"%name_tmp,list1)
        dim=dim+1
    print(X.shape)
    return X 
    
def generate_feature_step2(X):
    #第四次扩充，取倒数：
    c,r=X.shape
    dim=r
    index_tmp3=list(X.columns)
    for i in range(len(index_tmp3)):
        print("No:",i,'\n')
        c=[]
        a=X[index_tmp3[i]]
        for j in range(len(a)):
            if a[j]!=0:
                c.append(1/a[j])
            else:
                c.append(100000)
        name='1/'+index_tmp3[i]
        X.insert(dim,'%s'%name,c)
        dim=dim+1
    print(X.shape)
    return X 
    # WYdodWEZEKcLt1Lpt27Marn9lpqHgVPi