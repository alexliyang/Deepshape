# coding: utf-8


import numpy as np
import keras
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Dropout, Activation,Reshape
from keras import backend as K
from keras.layers.merge import concatenate
from keras.layers import Lambda, Dot
import numpy as np
import keras
from keras.models import Model
from keras import losses
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Dropout, Activation, Reshape
from keras import backend as K
from keras.layers.merge import concatenate
from keras.layers import Lambda, Dot
import seq2seq
from seq2seq.models import SimpleSeq2Seq
from seq2seq.models import Seq2Seq
from seq2seq.models import AttentionSeq2Seq
import tensorflow as tf

def binary_crossentropy_with_nan(y_true, y_pred):
    not_nan = tf.logical_not(tf.is_nan(y_true))
    y_true = tf.boolean_mask(y_true, not_nan)
    y_pred = tf.boolean_mask(y_pred, not_nan)
    return K.mean(K.binary_crossentropy(y_pred, y_true), axis=-1)
keras.losses.binary_crossentropy_with_nan = binary_crossentropy_with_nan


def binary_accuracy_with_nan(y_true, y_pred):
    not_nan = tf.logical_not(tf.is_nan(y_true))
    y_true = tf.boolean_mask(y_true, not_nan)
    y_pred = tf.boolean_mask(y_pred, not_nan)
    return K.mean(K.equal(y_true, K.round(y_pred)), axis=-1)
keras.metrics.binary_accuracy_with_nan = binary_accuracy_with_nan

def seq2seq_model(model_ind,en_depth =4, de_depth =5,dep=4,hid_dim = 10):

    #输入长度不可变！！
    if model_ind =='1':  
        encoder_depth = en_depth  #4
        decoder_depth = de_depth  #5
        model = SimpleSeq2Seq(input_dim=4, hidden_dim=hid_dim, #10
                        output_length=128, output_dim=1)
        model.compile(loss=binary_crossentropy_with_nan,
                      optimizer='rmsprop', depth=(encoder_depth, decoder_depth), metrics=[
                          binary_accuracy_with_nan])

    elif model_ind =='2':
        model = Seq2Seq(batch_input_shape=(
            None, 128, 4), hidden_dim=hid_dim, output_length=128, output_dim=1, depth=dep)
        model.compile(loss=binary_crossentropy_with_nan, optimizer='rmsprop', metrics=[
            binary_accuracy_with_nan])
    elif model_ind =='3':
        model = Seq2Seq(batch_input_shape=(None, 128, 4), hidden_dim=hid_dim,
                         output_length=128, output_dim=1, depth=dep, peek=True)
        model.compile(loss=binary_crossentropy_with_nan, optimizer='rmsprop', metrics=[
            binary_accuracy_with_nan])
    elif model_ind =='4':
        model = AttentionSeq2Seq(input_dim=4, input_length=128,
                                  hidden_dim=hid_dim, output_length=128, output_dim=1, depth=dep)
        model.compile(loss=binary_crossentropy_with_nan, optimizer='rmsprop', metrics=[
            binary_accuracy_with_nan])
    else:
        print 'no such model!'
    return model
