# -*-coding:utf-8-*-
from keras.layers import Input,Dense,Conv2D,AveragePooling2D,UpSampling2D, Flatten
import tensorflow as tf
from keras.layers import Concatenate
from keras.datasets import cifar10
from keras.models import Model
from keras.layers.core import Lambda
from keras.utils import np_utils
import numpy as np

def sub(args):
    y, B = args
    return tf.subtract(y, B)
#方差池化
def variance_pool(y,pool_size=(2, 2)):
    A = AveragePooling2D(pool_size=pool_size, strides=2, padding='valid')(y)
    B = UpSampling2D(size=pool_size)(A)
    C = Lambda(sub)([y,B])
    D = Lambda(lambda C: tf.square(C))(C)
    return D
#组卷积
def GConv2d(x, filters, kernel_size, strides=1, gconv_num=1):
    split = Lambda(lambda x: tf.split(x, num_or_size_splits=gconv_num, axis=-1))(x)
    x = Concatenate(axis=-1)([Conv2D((filters//gconv_num), kernel_size, strides=strides, padding='same')(inp) for inp in split])
    return x


if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = cifar10.load_data()
    x_train = np.array(x_train)
    y_train = np.array(y_train)
    x_test = np.array(x_test)
    y_test = np.array(y_test)
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    y_train = np_utils.to_categorical(y_train, 10)
    y_test = np_utils.to_categorical(y_test, 10)
    ip = Input(shape=(32, 32, 3))
    y = Conv2D(64, 3, strides=1,padding='same')(ip)
    y = Conv2D(128, 3, strides=2, padding='same')(y)
    y = Conv2D(128, 3, strides=2, padding='same')(y)
    y = Conv2D(128, 3, strides=1, padding='same')(y)
    # y2 = variance_pool(y,pool_size=(2, 2))
    # y3 = Concatenate(axis=-1)([y,y2])
    y = Conv2D(64, 1, strides=1, padding='same')(y)
    y = Conv2D(64, 1, strides=1, padding='same')(y)
    y =Flatten()(y)
    y = Dense(512)(y)
    y = Dense(216)(y)
    y = Dense(10, activation='softmax')(y)

    model = Model(ip, y)
    model.summary()
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])
    model.fit(x_train, y_train,
              batch_size=32,
              epochs=20,
              validation_data=(x_test, y_test),
              shuffle=True)

    model.save_weights('weights1.hdf5')
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test score:', score)
    print("Accuracy: %.2f%%" % (score[1] * 100))
