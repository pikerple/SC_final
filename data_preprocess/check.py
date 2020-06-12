import os
for i in os.listdir("/tmp2/b07902048/pic/unlabeled/"):
    if not os.path.isfile("/tmp2/b07902048/pic/unlabeled/{}/ok".format(i)):
        os.system("rm /tmp2/b07902048/pic/unlabeled/{} -rf".format(i))
