s = input()

n = input() #输入需要爬多少个楼梯
i = 1
t = []
while i <= int(n):
    t.append(input()) #每个楼梯的台阶数
    i += 1

#字符串不同元素个数：
si = input()
s = si.split(',')
t = {}
for item in s:
    if item in t.keys():
        pass
    else:
        t[item] = '1'

#多行，每行多个元素
import sys
line = sys.stdin.readline().strip()
values = list(map(int, line.split()))


#输出：
a = [1,3,2,5]
print(" ".join(str(s) for s in a))



# 多行输入：
line = sys.stdin.readlines()
value = []
for item in line:
	value.append(list(map(int, item.split())))


try:
    while True:
        line = sys.stdin.readline().strip()
        if line == '':
            break
        value = list(map(int, line.split()))
except:
    pass