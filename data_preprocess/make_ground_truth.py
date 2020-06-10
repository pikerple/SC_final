# -*- coding: utf-8 -*-
import os
import random
from os import path
import sys
from joblib import Parallel, parallel_backend, delayed
from constants import *
import shutil
num = 500
def separate_ground_truth():
    x = [[] for _ in range(128)]
    for i in range(1, num + 1):
        if os.path.isdir("{}{}".format(PIC_PATH, i)) and os.path.isfile("{}{}/ok".format(PIC_PATH, i)):
            truth_pth = "{}{}/{}_groundtruth.txt".format(MIR500_PATH, i, i)
            tmp = []
            with open(truth_pth, 'rt') as f:
                for line in f:
                    lines = list(map(float, line.split()))
                    tmp.append([lines[0]*1000, lines[1]*1000, int(lines[2])])

            now_time = FRAME_SIZE / 2
            idx = 1
            while now_time + FRAME_SIZE / 2 < tmp[-1][1]:
                exist = False
                for line in tmp:
                    if now_time >= line[0] and now_time < line[1]:
                        x[line[2]].append("{}{}/{}.png".format(PIC_PATH, i, idx))
                        exist = True
                        break
                if not exist:
                    x[0].append("{}{}/{}.png".format(PIC_PATH, i, idx))
                now_time += FRAME_SIZE - OVERLAP_SIZE
                idx += 1
            print('=== {} OK ==='.format(i))
    summ = 0
    for now in range(len(x)):
        summ += len(x[now])
        print(len(x[now]), end = " ")
    print()
    print('sum = ', summ)
    
    for now in range(128):
        random.Random(4).shuffle(x[now])
    new_x = []
    new_x.append(x[0])
    for k in range(LOWEST_SEMI, HIGHTEST_SEMI + 1):
        new_x.append(x[k])
    
    for now in range(len(new_x)):
        print(len(new_x[now]), end = " ")
    print()

    # output to dataset
    if not os.path.isdir(DATASET_PATH + "pic"):
        os.makedirs(DATASET_PATH + "pic", 0o755)
    with open(DATASET_PATH + "ground_truth", "w+t") as f:
        i = 0
        while i < DATASET_SIZE:
            for j in range(len(new_x)):
                if new_x[j]:
                    path = new_x[j].pop()
                    shutil.copyfile(path , "{}pic/{}.png".format(DATASET_PATH, i+1))
                    array = [0] * len(new_x)
                    array[j] = 1
                    f.write(" ".join(list(map(str, array))) + '\n')
                    i += 1
                    
                    if i % 1000 == 0:
                        print('finish {}'.format(i))
            
            
            
    

def main():
    
    separate_ground_truth()



if __name__ == "__main__":
    main()
