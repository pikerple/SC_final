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

tmp = []
with open("../ready", "rt") as f:
    for line in f:
        tmp.append(int(line))
arr = []
for i in range(1, 1501):
    if i not in tmp:
        arr.append(i)

youtube_list = []
with open(YOUTUBE_FILE_PATH, 'rt') as f:
    for line in f:
        youtube_list.append(line)
'''        
for i in arr:
    os.system('youtube-dl -x --audio-format mp3 -o "{}{}.%(ext)s" {}'.format(AUDIO_PATH, i, youtube_list[i-1]))
    print(i)

for i in arr:
    os.system("spleeter separate -i {}{}.mp3 -p spleeter:2stems -o {}".format(AUDIO_PATH, i, SEPARATE_PATH))
    print(i)
'''

def split_wav(dirs):
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

def f(i):
    try:
        split_wav(i)
    except:
        return

with parallel_backend(backend = "multiprocessing", n_jobs=-2):
    Parallel()(delayed(f)(str(i)) for i in arr)