# -*- coding: utf-8 -*-
import os
from os import path
import sys

from joblib import Parallel, parallel_backend, delayed
from constants import *
youtube_list = []

def download(i, pth):
    os.system('youtube-dl -x --audio-format wav -o "{}{}.%(ext)s" {}'.format(AUDIO_PATH, i, pth))

def main():
    with open(YOUTUBE_FILE_PATH, 'rt') as f:
        for line in f:
            youtube_list.append(line)
    with parallel_backend('multiprocessing', n_jobs=-2):
        Parallel()(delayed(download)(i+1, pth) for i, pth in enumerate(youtube_list))


if __name__ == "__main__":
    main()
