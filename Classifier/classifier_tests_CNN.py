#Made by Gerard Planella / Miquel Saula

from sklearn import neighbors, datasets
from sklearn.neural_network import MLPClassifier
import json
import random
import datetime
import numpy as np
import math
import pickle
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Convolution1D, Conv1D, MaxPooling1D, GlobalAveragePooling1D
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
from datetime import datetime
from sklearn import metrics

TOTAL_K_TO_TEST = 10
PERCENTAGE_TESTING = 0.15
PERCENTAGE_TOTAL = 1
ALPHA = 5e-4
MAX_VALUE = 1.0

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']

def normalize(data):
    maxv = 0.0
    index = 0

    for i in range(len(data)):
        v = data[i]
        if maxv < v:
            maxv = v
            index = i

    if maxv == 0:
        for i in range(len(data)): data[i] = 0
    else:
        scale_factor = MAX_VALUE / maxv
        for i in range(len(data)):
            data[i] = data[i]*scale_factor

    return data

print("Importing dataset...")

with open('spectrograms_testing.json') as f:
    data_testing = json.load(f)

with open('spectrograms_training.json') as f:
    data_training = json.load(f)

spectrograms_training = []
index_training = []

spectrograms_testing = []
index_testing = []

NUM_OF_SAMPLES = 40
NUM_OF_COMPONENTS = 13

random.shuffle(data_testing)
random.shuffle(data_training)

for i in range(0, int(len(data_testing))):
    stream = data_testing[i]["spectrograms_testing"]
    spectrogram = np.array(stream).reshape(NUM_OF_SAMPLES, NUM_OF_COMPONENTS)

    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index[data_testing[i]["classIndex_testing"]] = 1
    index = np.array(index).reshape(12)

    spectrograms_testing.append(spectrogram)
    index_testing.append(index)

for i in range(0, int(len(data_training))):
    stream = data_training[i]["spectrograms_training"]
    spectrogram = np.array(stream).reshape(NUM_OF_SAMPLES, NUM_OF_COMPONENTS)

    index = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index[data_training[i]["classIndex_training"]] = 1
    index = np.array(index).reshape(12)

    spectrograms_training.append(spectrogram)
    index_training.append(index)

print("Creating the model...")

ref = datetime.datetime.now()

 # 13 features - 25 components

model = 0
best_model = model
best_accuracy = 0

num_rows = len(spectrograms_training[0])
num_columns = len(spectrograms_training[0][0])
num_channels = 1
num_labels = len(classLabels)

spectrograms_training = np.array(spectrograms_training).reshape(np.array(spectrograms_training).shape[0], num_rows, num_columns, num_channels)
spectrograms_testing = np.array(spectrograms_testing).reshape(np.array(spectrograms_testing).shape[0], num_rows, num_columns, num_channels)

index_training = np.array(index_training).reshape(np.array(spectrograms_training).shape[0], num_labels)
index_testing = np.array(index_testing).reshape(np.array(spectrograms_testing).shape[0], num_labels)

print("Total training: " + str(len(spectrograms_training)))
print("Total testing: " + str(len(spectrograms_testing)))
print("Num rows: " + str(num_rows))
print("Num columns: " + str(num_columns))
print("Num channels: " + str(num_channels))

# Revisar la configuració de les capes de Pooling

# Construct model
model = Sequential()
model.add(Conv2D(filters=16, kernel_size=2, input_shape=(num_rows, num_columns, num_channels), activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))

model.add(Conv2D(filters=32, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=1))
model.add(Dropout(0.2))

model.add(Conv2D(filters=64, kernel_size=2, activation='relu'))
model.add(MaxPooling2D(pool_size=1))
model.add(Dropout(0.2))

model.add(Conv2D(filters=128, kernel_size=3, activation='relu'))
model.add(MaxPooling2D(pool_size=2))
model.add(Dropout(0.2))
model.add(GlobalAveragePooling2D())

model.add(Dense(num_labels, activation='softmax'))

# Compile the model
model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')

# Display model architecture summary
model.summary()

# Calculate pre-training accuracy
score = model.evaluate(spectrograms_testing, index_testing, verbose=1)
accuracy = 100*score[1]

print("Pre-training accuracy: %.4f%%" % accuracy)

num_epochs = 55#72
num_batch_size = 256

checkpointer = ModelCheckpoint(filepath='modelCNN.hdf5',
                               verbose=1, save_best_only=True)
start = datetime.now()

model.fit(spectrograms_training, index_training, batch_size=num_batch_size, epochs=num_epochs, validation_data=(spectrograms_testing, index_testing), callbacks=[checkpointer], verbose=1)

duration = datetime.now() - start
print("Training completed in time: ", duration)

# Evaluating the model on the training and testing set
score = model.evaluate(spectrograms_training, index_training, verbose=0)
print("Training Accuracy: ", score[1])

score = model.evaluate(spectrograms_testing, index_testing, verbose=0)
print("Testing Accuracy: ", score[1])

model_json = model.to_json()
with open("model_CNN.json", "w") as json_file:
    json_file.write(model_json)
