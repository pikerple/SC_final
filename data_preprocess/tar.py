from joblib import Parallel, parallel_backend, delayed
import os
from constants import *

def tar(i):
    os.system('tar -czvf /tmp2/b07902048/testset/{}.tgz {}{}'.format(i, PIC_PATH, i))

with parallel_backend('multiprocessing', n_jobs=-2):
    Parallel()(delayed(tar)(i) for i in os.listdir(PIC_PATH))
    
