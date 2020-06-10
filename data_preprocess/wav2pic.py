# -*- coding: utf-8 -*-
import os
from os import path
import sys
import wave
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from tempfile import NamedTemporaryFile
from scipy import signal
from scipy.io import wavfile
import librosa
import librosa.display
from joblib import Parallel, parallel_backend, delayed
from pydub import AudioSegment
from constants import *


def split_wav(dirs):
    ##ADD
    #if int(dirs) > 10:
    #    return
    ##ADD
    song_file = "{}{}/vocals.wav".format(SEPARATE_PATH, dirs)
    pic_dir = PIC_PATH + dirs + "/"
    if not os.path.isdir(pic_dir):
        os.makedirs(pic_dir, 0o755)
    ok_file = pic_dir + "ok"
    if not os.path.isfile(ok_file):
        with NamedTemporaryFile('w+t') as temp_file:
            newAudio = AudioSegment.from_wav(song_file)
            i = 0
            while i * (FRAME_SIZE - OVERLAP_SIZE) + FRAME_SIZE < len(newAudio):
                sliced = newAudio[i * (FRAME_SIZE - OVERLAP_SIZE) : i * (FRAME_SIZE - OVERLAP_SIZE) + FRAME_SIZE]
                sliced.export(temp_file.name, format="wav")
                plot_cqt(temp_file.name, pic_dir + str(i+1) + ".png")
                i += 1
            Path(ok_file).touch()
    print('ok')
            
        
def plot_cqt(song, path):
    plt.figure(figsize=(7.5, 3.75))
    y, sr = librosa.load(song)
    C = librosa.cqt(y, sr=sr)
    librosa.display.specshow(librosa.amplitude_to_db(C, ref=np.max), sr=sr)
    plt.axis('off')
    plt.savefig(path, bbox_inches="tight")
    plt.close('all')


def main():
    if not os.path.isdir(PIC_PATH):
        os.makedirs(PIC_PATH, 0o755)
    with parallel_backend(backend = "multiprocessing", n_jobs=-2):
        Parallel()(delayed(split_wav)(dirs) for dirs in os.listdir(SEPARATE_PATH))
            


if __name__ == "__main__":
    main()
