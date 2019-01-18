#coding:UTF8

import numpy as np
import matplotlib
import xlrd
#matplotlib.use('agg')
import matplotlib.pyplot as plt
ax=plt.subplot(111)
cor=[]
for i in range(20):
    li=[]
    li.append(5+i*3)
    li.append(100)
    cor.append(li)
#print(cor)

for i in range(len(cor)):
    ax.scatter(cor[i][0],cor[i][1])
    ax.plot([0,cor[i][0]],[0,cor[i][1]],c='b')
ax.plot([0,50],[40,40])
ax.plot([0,50],[50,50])
ax.plot([0,50],[60,60])
ax.plot([0,50],[70,70])
ax.scatter(0,0)
plt.show()