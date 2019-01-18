import time
time_start=time.time()
i=0
while i<10000:
    print i+1
    f=open('write-test','a')  
    f.write('123456789abcd\n')  
    f.close()
    i=i+1
time_end=time.time()
print "total time=",time_end-time_start,"s"