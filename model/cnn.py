import numpy as np
import keras
from keras.layers import Dense, Flatten, Reshape, Input
from keras.layers import Conv2D, MaxPooling2D, GlobalAveragePooling2D, Dropout
from keras.models import Sequential
from keras.callbacks import ModelCheckpoint, EarlyStopping, TensorBoard, CSVLogger
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from  skimage.measure import block_reduce
import random
from PIL import Image
import os, os.path
import sys
sys.path.append('../data_preprocess')
from constants import *
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

class AccuracyHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.acc = []

    def on_epoch_end(self, batch, logs={}):
        self.acc.append(logs.get('acc'))


def train(x_train, y_train, x_test, y_test):
    batch_size = 64
    epochs = 200

    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    img_x, img_y = 145, 49
    input_shape = (img_x, img_y, 3)
    num_classes = HIGHTEST_SEMI - LOWEST_SEMI + 2

    model = Sequential()
    model.add(Conv2D(32, kernel_size=(5,5), strides=(1,1),
        activation='tanh',
        input_shape=input_shape))
    model.add(Dropout(0.5))
    model.add(MaxPooling2D(pool_size=(2,2), strides=(2,2)))
    model.add(Conv2D(64, (3,3), activation='tanh'))
    model.add(Dropout(0.5))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Flatten())
    model.add(Dense(num_classes, activation='sigmoid'))
    model.compile(loss=keras.losses.binary_crossentropy,
            optimizer=keras.optimizers.Adam(lr=.0001, decay=1e-6),
            metrics=['accuracy'])

    history = AccuracyHistory()

    checkpoint = ModelCheckpoint(MODEL_PATH,
            monitor='val_loss',
            verbose=1,
            save_best_only=True,
            mode='min')
    early_stop = EarlyStopping(patience=5, 
            monitor='val_loss',
            verbose=1, mode='min')
    callbacks = [history, checkpoint, early_stop]
    print('shape = ', x_train.shape)
    model.fit(x_train, y_train,
            batch_size=batch_size,
            epochs=epochs,
            verbose=1,
            validation_data=(x_test, y_test),
            callbacks=callbacks)

    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    #plt.plot(range(1,7), history.acc)
    #plt.xlabel('Epochs')
    #plt.ylabel('Accuracy')
    #plt.savefig('loss.png')
    #plt.show()


def main():
    x, y = [], []
    for i in range(1, 10000 + 1):
        im = Image.open("{}pic/{}.png".format(DATASET_PATH, i))
        im = im.crop((10, 9, 591, 298))
        im = im.convert('RGB')
        resize = im.resize((49, 145), Image.NEAREST)
        resize.load()
        arr = np.asarray(resize, dtype=np.float32)
        arr /= 255.0
        x.append(arr)
        if i % 1000 == 0:
            print('=== now preprocess: {} ==='.format(i))
    print('x preprocess finish!')
    with open(DATASET_PATH + "ground_truth", "rt") as f:
        for line in f:
            y.append(list(map(float, line.split())))
    print('len: ', len(x), len(y))
        
        
    
                
    zipped = list(zip(x, y))
    #print(len(zipped))
    random.Random(4).shuffle(zipped)
    zipped = list(zip(*zipped))
    x_test = np.array(zipped[0][:len(zipped[0]) // 10])
    y_test = np.array(zipped[1][:len(zipped[0]) // 10])
    x_train = np.array(zipped[0][len(zipped[0]) // 10:])
    y_train = np.array(zipped[1][len(zipped[0]) // 10:])
    print(x_test.shape)
    
    train(x_train, y_train, x_test, y_test)

if __name__ == "__main__":
    main()
