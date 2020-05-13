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
from keras.models import model_from_json
from keras.optimizers import Adam
from keras.utils import np_utils
from sklearn import metrics

with open('spectrograms_testing.json') as f:
    data_testing = json.load(f)

spectrograms = []
index = []

NUM_OF_SAMPLES = 40
NUM_OF_COMPONENTS = 13

random.shuffle(data_testing)

for i in range(0, int(len(data_testing))):
    stream = data_testing[i]["spectrograms_testing"]
    spectrogram = np.array(stream).reshape(NUM_OF_SAMPLES, NUM_OF_COMPONENTS)

    indexaux = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    indexaux[data_testing[i]["classIndex_testing"]] = 1
    indexaux = np.array(indexaux).reshape(12)

    spectrograms.append(spectrogram)
    index.append(indexaux)

def load_trained_model(JSON_path, weights_path):
    json_file = open(JSON_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)

    model.load_weights(weights_path)
    return model

spectrograms = np.array(spectrograms).reshape(len(spectrograms), 40, 13, 1)
index = np.array(index).reshape(len(index), 12)

values = []

model = load_trained_model('model_CNN.json', 'modelCNN.hdf5')

num_iterations = 30

threshold = 0.9
step = 0.01

ratio = 1.0
newratio = 0.0
lastWasInc = True

while num_iterations != 0:
    ratio = newratio

    ratioaux = 0.0
    total = 0.0
    for i in range(len(spectrograms)):

        result = model.predict(spectrograms[i].reshape(1, 40, 13, 1))[0]
        maxval = result[np.argmax(result)]

        isCorrect = np.argmax(result) == np.argmax(index[i])

        total += 1.0
        if (maxval > threshold):
            if (isCorrect): ratioaux += 1.0
        else:
            if (not isCorrect): ratioaux += 1.0

    newratio = (total - ratioaux) / ratioaux
    if (newratio > ratio):
        if lastWasInc:
            threshold -= step
            lastWasInc = False
        else:
            threshold += step
            lastWasInc = True
    else:
        if (lastWasInc):
            threshold += step
        else:
            threshold -= step

    if (num_iterations > 20):
        step = 0.1
    elif (num_iterations > 10):
        step = 0.01
    else:
        step = 0.001

    print("-"*50)
    print("Iterations left: " + str(num_iterations))
    print("threshold: %.3f" % threshold)
    print("Ratio: " + str(ratio))
    print("Correct / Incorrect: " + str(int(ratioaux)) + "/" + str(int(total - ratioaux)))
    print("Failure: %.2f" % ((1 - ratioaux/total)*100.0))
    num_iterations -= 1
