#coding:utf8
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def generate_city(a,b): #随机生成城市坐标
    return np.random.randint(0,1000,size=[a,b])  
def getdistmat(coordinates):
    num = coordinates.shape[0]
    distmat = np.zeros((numcity,numcity))
    for i in range(num):
        for j in range(i,num):
            distmat[i][j] = distmat[j][i]=np.linalg.norm(coordinates[i]-coordinates[j])
    return distmat

numant = 50 #蚂蚁个数
numcity = 30 #城市数量
alpha = 2   #信息素重要程度因子
beta = 4    #启发函数重要程度因子
rho = 0.2   #信息素的挥发速度
Q = 1 #单个蚂蚁所携带的信息素的总量，用于走完以后更新每条走过的边的信息素
iter = 0
itermax = 301 #迭代次数

coordinates=generate_city(numcity,2) #生成城市坐标
distmat = getdistmat(coordinates)# 二维矩阵，计算每对节点的距离

'''
信息素因子反映了蚂蚁在移动过程中所积累的信息量在指导蚁群搜索中的相对重要程度，其值过大，蚂蚁选择以前走过的路径概率大，搜索随机性减弱；
值过小，等同于贪婪算法，使搜索过早陷入局部最优。实验发现，信息素因子选择[1,4]区间，性能较好。

m的数量很重要，因为m过大时，会导致搜索过的路径上信息素变化趋于平均，这样就不好找出好的路径了；m过小时，易使未被搜索到的路径信息素减小到0，
这样可能会出现早熟，没找到全局最优解。一般上，在时间等资源条件紧迫的情况下，蚂蚁数设定为城市数的1.5倍较稳妥。

启发函数因子 反映了启发式信息在指导蚁群搜索过程中的相对重要程度，其大小反映的是蚁群寻优过程中先验性和确定性因素的作用强度。过大时，虽然收敛速度会加快，
但容易陷入局部最优；过小时，容易陷入随机搜索，找不到最优解。实验研究发现，当启发函数因子为[3,4.5]时，综合求解性能较好。

信息素挥发因子 表示信息素的消失水平，它的大小直接关系到蚁群算法的全局搜索能力和收敛速度。实验发现，当属于[0.2，0.5]时,综合性能较好。

信息素强度，表示蚂蚁循环一周时释放在路径上的信息素总量，其作用是为了充分利用有向图上的全局信息反馈量，使算法在正反馈机制作用下以合理的演化速度搜索到全局最优解。
值越大，蚂蚁在已遍历路径上的信息素积累越快，有助于快速收敛。实验发现，当值属于[10,1000]时，综合性能较好
'''

etatable = 1.0/(distmat+np.diag([1e-10]*numcity)) #启发函数矩阵，表示蚂蚁从城市i转移到矩阵j的期望程度,np.diag()返回对角阵，方式为1/dij
#print(etatable)
pheromonetable  = np.ones((numcity,numcity)) # 信息素矩阵
pathtable = np.zeros((numant,numcity)).astype(int) #路径记录表

distmat = getdistmat(coordinates) #城市的距离矩阵

lengthaver = np.zeros(itermax) #各代路径的平均长度
lengthbest = np.zeros(itermax) #各代及其之前遇到的最佳路径长度
pathbest = np.zeros((itermax,numcity)) # 各代及其之前遇到的最佳路径长度

while iter < itermax:
    
    #本行为修改代码，随机产生每只蚂蚁的起点城市编号，pathtable存储每只蚂蚁的行走路径，是二维数组
    pathtable[:,0] = np.random.randint(0,numcity,size=[numant])  

    length = np.zeros(numant) #计算各个蚂蚁的路径总距离

    for i in range(numant):

        visiting = pathtable[i,0] # 当前所在的城市
        unvisited = set(range(numcity))#未访问的城市
        unvisited.remove(visiting) #删除元素

        for j in range(1,numcity):#循环numcity-1次，访问剩余的numcity-1个城市

            #用轮盘法选择下一个要访问的城市
            listunvisited = list(unvisited)

            probtrans = np.zeros(len(listunvisited))

            for k in range(len(listunvisited)): #轮盘赌法先依次计算每个未访问的城市的概率。
                #power(城市ij的信息素,alpha)/pow(城市ij的距离，alpha),etatable即为距离的倒数
                probtrans[k] = np.power(pheromonetable[visiting][listunvisited[k]],alpha) * np.power(etatable[visiting][listunvisited[k]],alpha)
                #probtrans为每个城市被选中的概率，即从i到j的概率，然后再计算总概率，即pij/P：
            cumsumprobtrans = (probtrans/sum(probtrans)).cumsum()
            #依次减去一个随机数，然后取第一个小于零的作为选择
            cumsumprobtrans -= np.random.rand() 

            #下一个要访问的城市,取cumsumprobtrans>0的元素集合的第一个元素作为listunvisited的索引，索引值给k
            k = listunvisited[list(np.where(cumsumprobtrans>0))[0][0]] 
            
            pathtable[i,j] = k #k值作为城市编号，赋给路径表，表示该蚂蚁在城市j时下一个将要访问的城市是k，

            unvisited.remove(k)

            length[i] += distmat[visiting][k] #第i只蚂蚁走过的路径长度累加一次

            visiting = k #将k作为下次循环的当前访问城市

        length[i] += distmat[visiting][pathtable[i,0]] #蚂蚁的路径距离包括最后一个城市和第一个城市的距离


    lengthaver[iter] = length.mean() #第iter轮的平均距离

    if iter == 0:
        lengthbest[iter] = length.min()
        pathbest[iter] = pathtable[length.argmin()].copy()       #所有蚂蚁中的最短路径长度的路径给pathbest
    else:
        if length.min() > lengthbest[iter-1]: #没有发现最短路径，将前一次的复制给当前次
            lengthbest[iter] = lengthbest[iter-1]
            pathbest[iter] = pathbest[iter-1].copy()

        else:
            lengthbest[iter] = length.min()
            pathbest[iter] = pathtable[length.argmin()].copy()    


    # 更新信息素
    changepheromonetable = np.zeros((numcity,numcity))
    for i in range(numant):
        for j in range(numcity-1):
            #计算每只蚂蚁走过的城市路径的信息素，根据城市间的距离和Q信息素总量计算
            changepheromonetable[pathtable[i,j]][pathtable[i,j+1]] += Q/distmat[pathtable[i,j]][pathtable[i,j+1]]

        changepheromonetable[pathtable[i,j+1]][pathtable[i,0]] += Q/distmat[pathtable[i,j+1]][pathtable[i,0]]

    pheromonetable = (1-rho)*pheromonetable + changepheromonetable#信息素挥发后剩下的加上本次更新后的作为最新的信息素

    print "1",pheromonetable.shape
    iter += 1 #迭代次数指示器+1

    if (iter-1)%10==0: 
        print(iter-1)


# 平均路径长度和最优长度        
fig,axes = plt.subplots(nrows=2,ncols=1,figsize=(12,10))
axes[0].plot(lengthaver,'k',marker = u'')
axes[0].set_title('Avg_length')
axes[0].set_xlabel(u'iteration')

axes[1].plot(lengthbest,'k',marker = u'')
axes[1].set_title('Shortest_length')
axes[1].set_xlabel(u'iteration')
fig.savefig('Average_Best.png',dpi=500,bbox_inches='tight')
plt.close()




for p in range(0,len(pathbest),100):
    #作出找到的最优路径图
    bestpath = pathbest[p]
    print bestpath
    print "start:",bestpath[0],"end:",bestpath[-1]

    plt.plot(coordinates[:,0],coordinates[:,1],'r.',marker=u'$\cdot$')
    plt.xlim([-100,coordinates[:,0].max()+100])
    plt.ylim([-100,coordinates[:,1].max()+100])
    for i in range(numcity-1):#
        m,n = int(bestpath[i]),int(bestpath[i+1])
        #print(m,n,type(int(m)))
        plt.plot([coordinates[m][0],coordinates[n][0]],[coordinates[m][1],coordinates[n][1]],'k')
    plt.plot([coordinates[int(bestpath[0])][0],coordinates[n][0]],[coordinates[int(bestpath[0])][1],coordinates[n][1]],'k') #起终点

    ax=plt.gca()
    ax.set_title("Shortest_length")
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y_axis')

    plt.savefig('Best Path'+str(p)+'.png',dpi=500,bbox_inches='tight')
    plt.close()




for i in range(coordinates.shape[0]):
    plt.scatter(coordinates[i][0],coordinates[i][1],s=10)
plt.savefig('scatter.png',dpi=500,bbox_inches='tight')