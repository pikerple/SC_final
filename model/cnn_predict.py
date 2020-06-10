import numpy as np
import keras
from keras.layers import Dense, Flatten, Reshape, Input
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard, CSVLogger
from keras.models import load_model

from  skimage.measure import block_reduce
from PIL import Image
import os, os.path
import sys
sys.path.append('../data_preprocess')
from constants import *
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

def main():
    x = []

    model = load_model(PRETRAIN_MODEL_PATH)
    model.compile(loss=keras.losses.binary_crossentropy,
                optimizer=keras.optimizers.Adam(),
                metrics=['accuracy'])

    for i in range(1, 2):
        for dirs in os.listdir(PIC_PATH + str(i)):
            if dirs == "ok":
                continue
            im = Image.open("{}{}/{}".format(PIC_PATH, i, dirs))
            im = im.crop((10, 9, 591, 298))
            im = im.convert('RGB')
            resize = im.resize((49, 145), Image.NEAREST)
            resize.load()
            arr = np.asarray(resize, dtype=np.float32)
            arr /= 255.0
            x.append(arr)
        x = np.array(x)
        y_pred = model.predict(x)
        notes_unsorted = [np.argmax(y_pred[n]) for n in range(len(y_pred))]
        print(notes_unsorted)
        sys.exit(0)
        #notes = [x for _,x in sorted(zip(filenums, notes_unsorted))]

        i = 0
        for note in notes:
            one_hot = np.zeros((128, 25))
            one_hot[note, :] = 1
            mid = utils.one_hot_to_pretty_midi(one_hot)
            mid.write('sample_outputs/daylight_' + str(i) + ".mid")
            i += 1
    
if __name__ == "__main__":
    main()