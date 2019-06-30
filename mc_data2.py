#coding=utf-8  

from keras.models import *  
from keras.layers import Input,Dense,Dropout,BatchNormalization,Conv2D,MaxPooling2D,AveragePooling2D,concatenate,Flatten, AtrousConvolution2D,MaxoutDense
from keras.layers.convolutional import Conv2D,MaxPooling2D,AveragePooling2D  
from keras.callbacks import ModelCheckpoint, LearningRateScheduler,TensorBoard,Callback,ReduceLROnPlateau
from keras.datasets import cifar10
from keras.utils import np_utils
import numpy as np  
import keras as K 
from keras.utils import plot_model
import cv2


batch_size=16
nb_epoch = 5000
classes=10
cbks = []
seed = 7  
np.random.seed(seed)  



def Conv2d_BN(x, nb_filter,kernel_size, padding='same',strides=(1,1),name=None):  
	if name is not None:  
	    bn_name = name + '_bn'  
	    conv_name = name + '_conv'  
	else:  
	    bn_name = None  
	    conv_name = None  

	x = Conv2D(nb_filter,kernel_size,padding=padding,strides=strides,activation='relu',name=conv_name)(x)  
	x = BatchNormalization(axis=3,name=bn_name)(x)  
	return x  


(x_train, y_train), (x_test, y_test) = cifar10.load_data()
'''
download_path ='/home/gpu4/Public/zx/jiaotong'
train_path=download_path+'/train'
test_path=download_path+'/data2'

y_train = []
x_train = []
imgs = os.listdir(train_path)
for img in imgs:
	
	if os.path.isfile(train_path + '/' + img):
		y_train.append(int(img.split('.',1)[0])/100)
		#print(type(y_train))
		img = cv2.imread(train_path + '/' + img)
		x_train.append(img)
		#print(train_path + '/' + img)

y_test = []
x_test = []
imgs = os.listdir(test_path)
for img in imgs:
	
	if os.path.isfile(train_path + '/' + img):
		y_test.append(int(img.split('.',1)[0])/100)
		#print(y_train)
		img = cv2.imread(train_path + '/' + img)
		x_test.append(img)
		#print(train_path + '/' + img)
'''

x_train=np.array(x_train)
y_train = np.array(y_train)
x_test = np.array(x_test)
y_test=np.array(y_test)

#print(np.shape(x_train))

x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.
img_rows=32
img_rows=32
nb_classes=10
nb_filter=64
nb_filter2=128
nb_filter3=256
kernel_size=(3,3)
strides=(1,1)
y_train = np_utils.to_categorical(y_train, classes)
y_test = np_utils.to_categorical(y_test, classes)




inpt = Input(shape=( 32,32,3))  

branch1x1 = Conv2d_BN(inpt,nb_filter,(1,1), padding='same',strides=(1,1),name=None)  
branch1x1 = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding='same')(branch1x1) 

branch3x3 = Conv2d_BN(inpt,nb_filter,(1,1), padding='same',strides=(1,1),name=None)  
branch3x3 = Conv2d_BN(branch3x3,nb_filter,(3,3), padding='same',strides=(1,1),name=None)  
branch3x3 = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding='same')(branch3x3) 

branch5x5 = Conv2d_BN(inpt,nb_filter,(1,1), padding='same',strides=(1,1),name=None)  
branch5x5 = Conv2D(nb_filter,(3,3), padding='same',strides=(1,1),name=None,dilation_rate=(2, 2))(branch5x5)
branch5x5 = BatchNormalization(axis=3)(branch5x5)
branch5x5 = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding='same')(branch5x5) 



branch1x1 = Conv2d_BN(branch1x1,nb_filter2,(1,1), padding='same',strides=(1,1),name=None)  


branch3x3 = Conv2d_BN(branch3x3,nb_filter2,(1,1), padding='same',strides=(1,1),name=None)  
branch3x3 = Conv2d_BN(branch3x3,nb_filter2,(3,3), padding='same',strides=(1,1),name=None)  


branch5x5 = Conv2d_BN(branch5x5,nb_filter2,(1,1), padding='same',strides=(1,1),name=None)  
branch5x5 = Conv2D(nb_filter2,(3,3), padding='same',strides=(1,1),name=None,dilation_rate=(2, 2))(branch5x5)
branch5x5 = BatchNormalization(axis=3)(branch5x5)



x = concatenate([branch1x1,branch3x3,branch5x5],axis=3)
x = Dropout(0.25)(x)

x = MaxPooling2D(pool_size=(3,3),strides=(2,2),padding='same')(x)

x = Conv2d_BN(x,nb_filter3,(1,1), padding='same',strides=(1,1),name=None)  
#x = Conv2d_BN(x,nb_filter,(3,3), padding='same',strides=(1,1),name=None)  

x = Conv2D(nb_filter3,(3,3), padding='same',strides=(1,1),name=None,dilation_rate=(1, 1))(x)
x = BatchNormalization(axis=3)(x)


x=AveragePooling2D(pool_size=(4, 4), strides=None, padding='valid', data_format=None)(x)
x=Flatten()(x)
x = Dropout(0.25)(x)
x = Dense(256,activation='relu')(x)  
x = Dropout(0.35)(x)
x = Dense(256,activation='relu')(x)
x = Dropout(0.25)(x)
x = Dense(classes,activation='softmax')(x)  



model = Model(inpt,x,name='inception')  
model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy'])  


model.summary()  

tb = TensorBoard(log_dir='./mc_data2_logs', histogram_freq=1, write_graph=True, write_images=False, embeddings_freq=0,
					embeddings_layer_names=None, embeddings_metadata=None)
#model_checkpoint = ModelCheckpoint('mc_weights2.hdf5', monitor='loss', verbose=1, save_best_only=True)


model.fit(x_train, y_train,
		  batch_size=batch_size,
		  epochs=nb_epoch,
		  validation_data = (x_test, y_test),
		  shuffle=True,
		  callbacks=[tb])
plot_model(model, to_file='mc_model.png',show_shapes=True)
model.save_weights('mc_weights2.hdf5')