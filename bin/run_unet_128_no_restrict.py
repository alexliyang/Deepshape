import numpy as np
import datetime
import argparse
import sys,os,errno,gc,sys
from glob import glob
import pandas as pd
import h5py
from tqdm import tqdm
import keras as K
sys.path.append('bin')
from keras.callbacks import TensorBoard
from keras.callbacks import EarlyStopping
from unet_128_model_no_restict import *
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # so the IDs match nvidia-smi
os.environ["CUDA_VISIBLE_DEVICES"] = "5"
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

parser = argparse.ArgumentParser()
parser.add_argument('-m', dest='model_path')
parser.add_argument('-s', dest='save_path')
parser.add_argument('-c', dest='count')
parser.add_argument('-i', dest='input_data')
#parser.add_argument('-c', dest='count')
args = parser.parse_args()

def get_data(count):
    with h5py.File(args.input_data+'_'+str(count)) as f:
        x_train = f['train_images'][:]
        y_train = f['y_train'][:]
    return x_train, y_train

def data_generator(data, labels, batch_size):
    batches = (data.shape[0] + batch_size - 1)//batch_size
    while(True):
        for i in range(batches):
            X = data[i*batch_size: (i+1)*batch_size]
            Y = labels[i*batch_size: (i+1)*batch_size]
            yield (X, Y)

model = UNET_128()
optim = Adam()
model.compile(optimizer=optim, loss=binary_crossentropy_with_nan,
              metrics=[binary_accuracy_with_nan, mse_with_nan])

def Model(X_train, Y_train, batch_size=64, num_epochs=100):
    #model_checkpoint = ModelCheckpoint(args.model_path,
               #         monitor='binary_accuracy_with_nan', save_best_only=True)  model_checkpoint,
    callbacks = [ EarlyStopping(monitor='CrossEntropyLoss',
        patience=10, verbose=0), TensorBoard(log_dir='deepshape/output/tensorboard/unet/log_dir')]

    model.fit_generator(generator=data_generator(X_train, Y_train, batch_size),
                        steps_per_epoch=(
                            X_train.shape[0] + batch_size - 1) // batch_size,
                        epochs=num_epochs, verbose=1, callbacks=callbacks)

    model.save(args.save_path)

for i in range(int(args.count)):
    x_train, y_train = get_data(i)
    Model(x_train, y_train, 64, 100)
    gc.collect()
