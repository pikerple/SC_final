# -*- coding: utf-8 -*-
import os
from os import path
import sys
from joblib import Parallel, parallel_backend, delayed
from constants import *

def separate(dirs):
    print(dirs.replace(".wav", ""))
    if dirs.replace(".wav", "") not in os.listdir(SEPARATE_PATH):
        os.system("spleeter separate -i {}{} -p spleeter:2stems -o {}".format(AUDIO_PATH, dirs, SEPARATE_PATH))

def main():
    with parallel_backend('multiprocessing', n_jobs=4):
        Parallel()(delayed(separate)(dirs) for dirs in os.listdir(AUDIO_PATH))

if __name__ == "__main__":
    main()
