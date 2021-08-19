# from functools import lru_cache
H,W = 1,8

def singleLayer(W):
    result = []
    def dp(tem):
        if tem[-1] == W:
            result.append(tem)
        else:
            if tem[-1]+2 <= W:
                dp(tem+[tem[-1]+2])
            if tem[-1]+3 <= W:
                dp(tem+[tem[-1]+3])
    dp([0])
    return result
def canBeNeighbor(l1,l2):
    return len(set(l1+l2)) == len(l1)+len(l2)-2

resultSL = singleLayer(W)
print(resultSL);
n = len(resultSL)
matrix = [[0]*n for i in range(n)]

print(len(resultSL))

for i in range(len(resultSL)-1):
    for j in range(i+1,len(resultSL)):
        if canBeNeighbor(resultSL[i],resultSL[j]):
            matrix[i][j] = matrix[j][i] = 1

current = tuple(range(len(resultSL)))
# print(current)
# import functools
# @functools.lru_cache()
def dp(current,layer):
    if layer == H:
        return len(current)
    res = 0
    for cur in current:
        curNew = tuple([i for i in range(len(resultSL)) if matrix[i][cur]==1])
        res += dp(curNew,layer+1)
    return res

print(dp(current,1))
