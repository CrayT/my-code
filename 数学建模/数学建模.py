
# coding: utf-8

# In[72]:


import sympy
import copy
import copy
import numpy as np
line=[[60600,69982,7995],[61197,69928,7980],[61790,69838,7955],[62377,69713,7920],
      [62955,69553,7875],[63523,69359,7820],[64078,69131,7755],[64618,68870,7680],
      [65141,68577,7595],[65646,68253,7500],[66131,67900,7395],[66594,67518,7280],
      [67026,67116,7155],[67426,66697,7020],[67796,66263,6875],[68134,65817,6720],
      [68442,65361,6555],[68719,64897,6380],[68966,64429,6195],[69184,63957,6000]]
radars=[[80000,0,0],[130000,60000,0],[30000,60000,0],[55000,110000,0],[105000,110000,0]]
def Drone(t):
    result=[]
    for i in radars:
        ratio=[t[0]-i[0],t[1]-i[1],t[2]-i[2]]
        result.append(ratio)
    return result
vectors=[]
for i in line:
    vectors.append(Drone(i))
# print(vectors)


# In[73]:


##r代表雷达序号，v代表组号
def sofun(r1,r2,r3,v1,v2,v3):
    ax,ay,az,bx,by,bz,cx,cy,cz,dx,dy,dz = sympy.symbols("ax,ay,az,bx,by,bz,cx,cy,cz,dx,dy,dz")
    eq1 = (ax-radars[r1][0])/vectors[v1][r1][0]-(az-radars[r1][2])/vectors[v1][r1][2]
    eq2 = (ay-radars[r1][1])/vectors[v1][r1][1]-(az-radars[r1][2])/vectors[v1][r1][2]
    eq3 = (bx-radars[r2][0])/vectors[v2][r2][0]-(bz-radars[r2][2])/vectors[v2][r2][2]
    eq4 = (by-radars[r2][1])/vectors[v2][r2][1]-(bz-radars[r2][2])/vectors[v2][r2][2]
    eq5 = (cx-radars[r3][0])/vectors[v3][r3][0]-(cz-radars[r3][2])/vectors[v3][r3][2]
    eq6 = (cy-radars[r3][1])/vectors[v3][r3][1]-(cz-radars[r3][2])/vectors[v3][r3][2]
    eq7 = (ax-bx)/(ax-cx)-(az-bz)/(az-cz)
    eq8 = (ay-by)/(ay-cy)-(az-bz)/(az-cz)
    eq9 = (ax-bx)/(v2-v1)-(bx-cx)/(v3-v2)
    eq10 = (ay-by)/(v2-v1)-(by-cy)/(v3-v2)
    eq11 = (az-bz)/(v2-v1)-(bz-cz)/(v3-v2)
    eqs=[eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9,eq10,eq11]
    re = sympy.solve(eqs, [ax,ay,az,bx,by,bz,cx,cy,cz],check=False,rational=True)
#     if re and re[0][2]>=2000 and re[0][5]>=2000 and re[0][8]>=2000 and re[0][2]<=2500 and re[0][5]<=2500 and re[0][8]<=2500:
    if re:
        res=[]
        for i in re:
            print(toFloat(list(i)))
            try:
                if i[2]>=2000 and i[5]>=2000 and i[8]>=2000 and i[2]<=2500 and i[5]<=2500 and i[8]<=2500:
                    res.append(list[i])
            except:
                pass
        if res:
            res.append([v1,v2,v3])
            print(res)
        return res
    else:
        return []

def toFloat(a):
    for i in range(len(a)):
        a[i]=float(a[i])
    return a
re=sofun(0,1,2,0,1,2)
print(re)


# In[ ]:


results=[]
zz=0
for i in range(1):
    for j in range(i+1,2):
        for k in range(j+1,3):
            for l in range(5):
                for m in range(5):
                    for n in range(5):
                        re=sofun(l,m,n,i,j,k)
                        if zz%1000==0:
                            print(zz)
                        zz+=1
                        if re:
                            print(zz,':',re)
                            if len(re)>2:
                                print(re)
                            results.append(re)


# In[74]:


def sodis(r,h):
    points=[]
    for i in line:
        x=(i[0]-r[0])*h/i[2]+r[0]
        y=(i[1]-r[1])*h/i[2]+r[1]
        points.append([x,y])
    return points
def dist(a,b):
    return ((a[0]-b[0])**2+(a[1]-b[1])**2)**0.5
paths=[]
points_all=[]
for r in radars:
    for h in [2000,2100,2200,2300,2400,2500]:
        points=sodis(r,h)
        points_all.append(points)
        path=[]
        for i in range(20):
            for j in range(i+1,20):
                tem=dist(points[i],points[j])
                tem=tem/(j-i)
#                 if j==19 and tem<=500:
#                     print(tem,h,r)
                if tem>=1000/3 and tem<=500:
                    path.append([i,j])
        paths.append(path)


# In[80]:


demo=np.zeros(20).tolist()
result=[]
def test(de,a):
    if de[a[0]]<3 and de[a[1]]<3:
        return True
    else:
        return False
def check_de(de,maxi,result):
    tem=sum(de)
    if tem>maxi[0]:
        maxi[0]=tem
        print(maxi[0])
        print(de)
        print(result)
    if tem==60:
        return True
    else:
        return False
def recur(maxi,de,result,num):
#     if sum(de)>52:
#         print(de)
#     if de[0]>0:
#         print(de)
    de=copy.deepcopy(de)
    result=copy.deepcopy(result)
    if check_de(de,maxi,result):
        return result
    for i in paths[num]: 
        if test(de,i):
            de[i[0]]+=1
            de[i[1]]+=1
            result.append(i)
            tem = recur(maxi,de,result,num+1)
            if tem:
                return tem
            else:
                de[i[0]]-=1
                de[i[1]]-=1
                result.pop()
    return False
maxi=[0]
re=recur(maxi,demo,result,0)
print(re)


# In[81]:


use=np.zeros(30)
result=[[]]*30
maxi=[0]
def check_de(de,maxi,result,use,aban):
    tem=sum(de)
    test=[de[i] for i in range(20) if i not in aban]
    if tem>maxi[0]:
        maxi[0]=tem
        print(maxi[0])
        print(de)
        print(result)
        print(use)
        print(aban)
    if sum(test)==len(test)*3:
        return True
    else:
        return False
def find_urgent(use,demo,aban):
    demo2=np.zeros(20).tolist()
    mini=9999
    for i in range(len(paths)):
        if use[i]:
            continue
        for j in paths[i]:
            if demo[j[0]]<3 and demo[j[1]]<3:
                demo2[j[0]]+=1
                demo2[j[1]]+=1
    for i in range(len(demo2)):
        if demo[i]==3 or i in aban:
            demo2[i]=9999
#     print(demo2)
    urg = demo2.index(min(demo2))
    return urg
def find_now(demo):
    for i in demo:
        if i<3:
            return demo.index(i)
    return -1
def find_position(num,demo,use):
    result=[]
    for i in range(len(paths)):
        if use[i]:
            continue
        for j in paths[i]:
            if num in j and demo[sum(j)-num]<3:
                result.append([i,j])
    return result
#     while True:
#         end=True
#         for i in range(len(result)-1):
#             if sum(result[i][1])>sum(result[i+1][1]):
#                 result[i],result[i+1]=result[i+1],result[i]
#                 end=False
#         if end:
#             return result
def recur2(demo,result,use,maxi,aban):
    demo=copy.deepcopy(demo)
    result=copy.deepcopy(result)
    use=copy.deepcopy(use)
    if check_de(demo,maxi,result,use,aban):
        return result
#     now=find_now(demo)
    now=find_urgent(use,demo,aban)
#     print(now)
    pos=find_position(now,demo,use)
    while not pos:
        aban.append(now)
        now=find_urgent(use,demo,aban)
        pos=find_position(now,demo,use)
    for p in pos:
        demo[p[1][0]]+=1
        demo[p[1][1]]+=1
        result[p[0]]=p[1]
        use[p[0]]+=1
        tem=recur2(demo,result,use,maxi,aban)
        if tem:
            return result
        demo[p[1][0]]-=1
        demo[p[1][1]]-=1
        result[p[0]]=[]
        use[p[0]]=0
    print('False')
    return False
aban=[]
re=recur2(demo,result,use,maxi,aban)
print(re)


# In[22]:


demo0=np.zeros(20)
demo2=np.zeros(20)
demo3=[copy.deepcopy([]) for i in range(20)]
# print(demo3)
for path in paths:
    tem=np.zeros(20)
    for i in path:
        demo0[i[0]]+=1
        demo0[i[1]]+=1
        tem[i[0]]=1
        tem[i[1]]=1
        index=paths.index(path)
#         print(demo3,demo3[i[0]],index)
        if index not in demo3[i[0]]:
            demo3[i[0]].append(index)
        if index not in demo3[i[1]]:
            demo3[i[1]].append(index)
#         print(i,demo3)
    demo2+=tem
print(demo0.tolist())
print(demo2.tolist())
for i in demo3:
    print(i)
for i in range(len(paths)):
    print(find_position(i,demo,use))


# In[20]:


# print(re)
# print(points_all)
data=[]
for i in range(29):
    a=points_all[i][re[i][0]]
    b=points_all[i][re[i][1]]
    c=i%6*100+2000
    a.append(c)
    b.append(c)
    data.append([a,b])
print(data)


# In[27]:


a=1
b=[2]
def demo():
    print(b)
    print(a)
    demo()
demo()

