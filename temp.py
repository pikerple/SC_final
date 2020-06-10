import os
count = 0
for i in range(1, 501):  
    if os.path.isfile('/tmp2/b07902048/pic/labeled/{}/ok'.format(i)):
        count+=1
print(count)
