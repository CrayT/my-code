num=input("input:")
A=[]
for i in range(int(num)):
    #ss=str("输入：")
    print(i)
    A.append(str(input("输入:")))
FF=[]
for item in A:
    if item[0] in FF:
        pass
    else:
        FF.append(item[0])
print(FF)
for item in range(len(FF)):
    pass