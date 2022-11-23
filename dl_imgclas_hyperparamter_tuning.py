# -*- coding: utf-8 -*-
"""DL_IMGCLAS_HYPERPARAMTER_TUNING.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TNGg8S_-CwgNgZxvoCLz-sTt8-urp2Fy
"""

#https://youtu.be/zBOavqh3kWU
# CLASSIFICATION OF IMAGE DATASET TO LEARN THE  IMAGE FEATURE AND CLASSIFY THE UNKNOWN INTO  VARIOUS CATEGORIES
# APPLYING RESNET ON THE DATASET CATEGORSING ANIMALS, VEHICLES, PLANETS, HUMANS, ASTEROIDS, PLANTS, MOUNTAINS, BOOKS , MOBILES, FOOD
# Data category = 10

#!pip install qiskit-machine-learning

from keras.models import  Sequential
from keras import models, layers
import tensorflow as tf
from keras.layers import Flatten, Dense, Conv2D, MaxPooling2D
import matplotlib.pyplot as plt
import numpy as np
from keras.layers.core.activation import Activation
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow_hub as hub
import PIL.Image as Image
# from tensorflow.keras.applications.resnet50 import ResNet50
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
# from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img
# from tensorflow.keras.models import Sequential, load_model
# from tensorflow.keras.layers import Input, Lambda, Dense, Flatten
# from tensorflow.keras.models import Model
from glob import glob
import os
import seaborn as sns
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, InputLayer
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
import cv2
#from qiskit import algorithms

IMG_WIDTH=200
IMG_HEIGHT=200

def create_dataset(img_folder):
   
    img_data_array=[]
    class_name=[]
   
    for dir1 in os.listdir(img_folder):
        for file in os.listdir(os.path.join(img_folder, dir1)):
       
            image_path= os.path.join(img_folder, dir1,  file)
            image= cv2.imread( image_path, cv2.COLOR_BGR2RGB)
            image=cv2.resize(image, (IMG_HEIGHT, IMG_WIDTH),interpolation = cv2.INTER_AREA)
            image=np.array(image)
            image = image.astype('float32')
            image /= 255 
            img_data_array.append(image)
            class_name.append(dir1)
    return img_data_array, class_name

trainSet_Path = "/content/drive/MyDrive/Colab Notebooks/Train" 
#https://drive.google.com/drive/folders/1WHR55HYdYsajCFM0URpkZj6VZ2qfP0sS?usp=sharing
#Test
testSet_Path = "/content/drive/MyDrive/Colab Notebooks/Test"
#https://drive.google.com/drive/folders/15euCQaubjtaNaVrhUBRdkNOkIlz_gMoK?usp=sharing

img_data, class_name =create_dataset(trainSet_Path)

target_dict={k: v for v, k in enumerate(np.unique(class_name))}
print(target_dict)

target_val=  [target_dict[class_name[i]] for i in range(len(class_name))]
print(target_val)

from keras.layers.serialization import activation
from scipy.ndimage.morphology import filters
from keras.engine import input_layer

# model = tf.keras.models.Sequential()
# model.add(tf.keras.layers.MaxPooling2D(pool_size=(2, 2),
#    input_shape=(4,4,1)))
# model.compile('adam', 'mean_squared_error')


model = tf.keras.Sequential(
    [  
      # first convolution layer
      tf.keras.layers.Conv2D(32, (3, 3), activation="relu",
                          input_shape=(200, 200, 3)),
      tf.keras.layers.MaxPooling2D((2, 2), strides=2),

      # second convolution layer
      tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
      tf.keras.layers.MaxPooling2D((2, 2), strides=2),

      # fully connected classification
      # single vector
      tf.keras.layers.Flatten(),
      
      # hidden layer and output layer
      tf.keras.layers.Dense(1024, activation="relu"),
      tf.keras.layers.Dense(10, activation="softmax")
     
    ]
)


model.compile(optimizer='rmsprop',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

history = model.fit(x=np.array(img_data, np.float32),
                    y=np.array(list(map(int,target_val)),np.float32), epochs=10, E)



#RESNET

"""**RESNET TRAINING on SAME SAMPLES**

"""

IMAGE_SHAPE = [224,224]

resnetModel = ResNet50(weights='imagenet',include_top=False, input_shape=IMAGE_SHAPE+[3])

for layers in resnetModel.layers:
  layers.trainable= False

folders = glob(trainSet_Path+"/*")
folders

x = Flatten()(resnetModel.output)

predict = Dense(len(folders), activation='softmax')(x)

model = Model(inputs = resnetModel.input,  outputs= predict )

model.summary()

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

train_data = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_data = ImageDataGenerator(rescale=1./255)

train_set = train_data.flow_from_directory(trainSet_Path, target_size=(224,224), batch_size=32, class_mode='categorical')

test_set = test_data.flow_from_directory(testSet_Path, target_size=(224,224), batch_size=32, class_mode='categorical')

modelSave = model.fit(train_set, validation_data=test_set, epochs=10, steps_per_epoch=len(train_set), validation_steps=len(test_set))

plt.plot(modelSave.history['loss'], label='train loss')
plt.plot(modelSave.history['val_loss'], label='val loss')
plt.legend()
plt.show()

plt.plot(modelSave.history['accuracy'], label='train accuracy')
plt.plot(modelSave.history['val_accuracy'], label='val accuracy')
plt.legend()
plt.show()

y_pred = model.predict(test_set)
y_pred = np.argmax(y_pred, axis=1)

y_pred

imgtoTest = image.load_img('/content/drive/MyDrive/Colab Notebooks/food.jpg', target_size=(224,224))

imgtoTest

find = np.array(imgtoTest)
find

find = find/255

find

find.shape

find = np.expand_dims(find, axis=0)

find.shape

findResult = np.argmax(model.predict(find), axis=1)

findResult



