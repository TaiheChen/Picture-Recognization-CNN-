# -*- coding: utf-8 -*-
"""CNNHYF.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IUSBoutrGEyz27hFB3tMD_fIlJExtYKM
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os, time
import matplotlib.pyplot as plt
#from keras.datasets import fashion_mnist
from sklearn.model_selection import train_test_split
import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
#from keras.layers.advanced_activations import LeakyReLU
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16;
from keras.applications.vgg16 import preprocess_input
import os

# don't need if using your data
import keras
#from keras.applications import VGG19
#from keras.applications.vgg19 import preprocess_input
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.models import Model
from keras import models
from keras import layers
from keras import optimizers

# Commented out IPython magic to ensure Python compatibility.
def load_mnist(path, kind='train'):
    import os
    import gzip
    import numpy as np

    """Load MNIST data from `path`"""
    labels_path = os.path.join(path,
                               '%s-labels-idx1-ubyte.gz'
#                                % kind)
    images_path = os.path.join(path,
                               '%s-images-idx3-ubyte.gz'
#                                % kind)

    with gzip.open(labels_path, 'rb') as lbpath:
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8,
                               offset=8)

    with gzip.open(images_path, 'rb') as imgpath:
        images = np.frombuffer(imgpath.read(), dtype=np.uint8,
                               offset=16).reshape(len(labels), 784)

    return images, labels

from google.colab import drive
drive.mount('/content/drive')

X_train = pd.read_pickle( './drive/My Drive/Train.pkl')
y_train = np.genfromtxt('./drive/My Drive/TrainLabels.csv', delimiter=',')
X_test = pd.read_pickle('./drive/My Drive/Test.pkl')

#X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.0, random_state=13) # trainign and validation
#X_train.shape
#x_train, y_train = X, y
#plt.imshow(X_train[0])

print(X_train.shape)
plt.imshow(X_train[1])

# Each image's dimension is 32 x 32
from keras.preprocessing.image import img_to_array, array_to_img

img_rows, img_cols = 64, 128
img_rows_new, img_cols_new = 64, 128 # 64, 64 -> increase/decrease 
input_shape = (img_rows, img_cols, 1)

# Prepare the training images
X_train = np.stack([X_train]*3, axis=-1)
X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, 3)
#X_train = np.asarray([img_to_array(array_to_img(im, scale=False).resize((img_rows_new,img_cols_new))) for im in X_train]) 
X_train = X_train.astype('float32')
X_train /= 255.0

# Prepare the test images
X_test = np.stack([X_test]*3, axis=-1)
X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, 3)
#X_test = np.asarray([img_to_array(array_to_img(im, scale=False).resize((img_rows_new,img_cols_new))) for im in X_test]) 
X_test = X_test.astype('float32')
X_test /= 255.0

from keras.layers import Conv2D, MaxPool2D
from keras.layers import Dense, Flatten
from keras.models import Sequential
from keras.utils import to_categorical
y_train = to_categorical(y_train)

model = Sequential()
model.add(Conv2D(32, kernel_size=(5,5), activation='relu', input_shape=(img_rows, img_cols, 3)))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Conv2D(64, kernel_size=(5,5), activation='relu'))
model.add(MaxPool2D(pool_size=(2,2), strides=(2,2)))
model.add(Flatten())
model.add(Dense(1000, activation='relu'))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=128, epochs=20,validation_split=0.2)

from keras.layers import Conv2D, MaxPool2D
from keras.layers import Dense, Flatten, Activation
from keras.models import Sequential
from keras.utils import to_categorical
from keras.optimizers import Adam
y_train = to_categorical(y_train)

model = Sequential()
model.add(Conv2D(32, (3, 3), padding='same',  # 32，(3,3)是卷积核数量和大小
                 input_shape=(img_rows, img_cols, 3)))  # 第一层需要指出图像的大小
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(10))
model.add(Activation('softmax'))

# initiate RMSprop optimizer
opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)

# Let's train the model using RMSprop
model.compile(loss='categorical_crossentropy',
              optimizer=opt,
              metrics=['accuracy'])

pre = model.predict_classes(X_test)

import numpy as np
np.savetxt('ExampleSubmissionRandom.csv', pre, delimiter = ',')

from google.colab import files
files.download('ExampleSubmissionRandom.csv')

import keras
#from keras.applications import VGG19
#from keras.applications.vgg19 import preprocess_input
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
from keras.layers import Dense, Dropout
from keras.models import Model
from keras import models
from keras import layers
from keras import optimizers

# Create the base model of VGG19
vgg19 = ResNet50(weights='imagenet', include_top=False, input_shape = (img_rows_new, img_cols_new, 3), classes = 10) 


# Preprocessing the input 
X_train = preprocess_input(X_train)
#X_val = preprocess_input(X_val)
X_test = preprocess_input(X_test)

# Extracting features
train_features = vgg19.predict(np.array(X_train), batch_size=256, verbose=1)
test_features = vgg19.predict(np.array(X_test), batch_size=256, verbose=1)
#val_features = vgg19.predict(np.array(X_val), batch_size=256, verbose=1)

# Flatten extracted features
train_features = np.reshape(train_features, (60000, 4*4*1024))
test_features = np.reshape(test_features, (10000, 4*4*1024))
#val_features = np.reshape(val_features, (12000, 4*4*1024))

# Add Dense and Dropout layers on top of VGG19 pre-trained
model = models.Sequential()
model.add(layers.Dense(2048, activation='relu', input_dim=4 * 4 * 1024))
#model.add(layers.Dropout(0.25))
model.add(layers.Dense(1024, activation='relu'))
#model.add(layers.Dropout(0.25))
#model.add(layers.Dropout(0.25))
model.add(layers.Dense(512, activation='relu'))
model.add(layers.Dense(10, activation="softmax"))

# Compile the model
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])

vgg = VGG16(include_top=False, weights='imagenet', 
                                     input_shape=(img_rows_new, img_cols_new, 3))

output = vgg.layers[-1].output
output = keras.layers.Flatten()(output)
output = Dense(10, activation='softmax')(output)

vgg_model = Model(vgg.input, output)

vgg_model.trainable = True
for layer in vgg_model.layers[:6]:
    layer.trainable = False
vgg_model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])

y = to_categorical(np.array(y_train))

# Train the the model
history = model.fit(
    train_features,
    y,
    epochs=50
)

prediction = model.predict_classes(test_features)



prediction

prediction_df = pd.DataFrame(index = None)
prediction_df["id"] = [i for i in range(0, len(prediction))]
prediction_df["output"] = prediction
prediction_df.to_csv("submission.csv",index=False )

model.fit_generator(datagen.flow(x_train, y_train,
                                         batch_size=batch_size),
                            steps_per_epoch=x_train.shape[0] // batch_size,
                            epochs=epochs,
                            validation_data=(x_val, y_val),shuffle=True,verbose=1)