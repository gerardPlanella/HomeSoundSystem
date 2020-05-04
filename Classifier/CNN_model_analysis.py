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

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']
classLabelsCmp = ['C', 'FA', 'BW', 'GB', 'D', 'F', 'CF', 'HB', 'R', 'H', 'RW', 'S']

labels_to_skip = [2, 3, 7, 8, 10]

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

    indaux = data_testing[i]["classIndex_testing"]
    skip = False
    for v in labels_to_skip:
        if (indaux == v): skip = True
    if (skip): continue

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
resultsCorrect = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
resultsCorrupting = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
resultsTotal = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
results = []
for i in range(12): results.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])

for i in range(len(spectrograms)):

    result = model.predict(spectrograms[i].reshape(1, 40, 13, 1))[0]
    maxval = result[np.argmax(result)]

    val2 = 0
    for v in result:
        if (val2 < v and v != maxval):
            val2 = v

    isCorrect = np.argmax(result) == np.argmax(index[i])

    resultsTotal[np.argmax(index[i])] += 1.0
    if (isCorrect): resultsCorrect[np.argmax(index[i])] += 1.0
    else: resultsCorrupting[np.argmax(result)] += 1.0
    results[np.argmax(index[i])][np.argmax(result)] += 1.0

    #if (not isCorrect):
    #    values.append(maxval)

        #print("-"*50)
        #print("Result:   " + str(result))
        #print("Original: " + str(index[i]))
        #print("Confidence: " + str(maxval * 100.0))
        #print("Correct: " + str(isCorrect))
        #print("Difference: " + str(float(maxval) - float(val2)))

values.sort()
#ACCEPTANCE = 1

#print(values[int(len(values)*ACCEPTANCE)-1])

print("\n"*2)
print(" <---   ENCERTS PER EVENT   ---> \n")
print("-"*50)
for i in range(len(classLabels)):
    if (not i in labels_to_skip):
        if (i == 5 or i == 8 or i == 9):
            print(classLabels[i] + ": \t\t%.2f" % ((resultsCorrect[i]/resultsTotal[i])*100.0), end='')
            print("%", end='')
            print(" (" + str(int(resultsCorrect[i])) + "/" + str(int(resultsTotal[i])) + ")")
        else:
            print(classLabels[i] + ": \t%.2f" % ((resultsCorrect[i]/resultsTotal[i])*100.0), end='')
            print("%", end='')
            print(" (" + str(int(resultsCorrect[i])) + "/" + str(int(resultsTotal[i])) + ")")
print("-"*50 + "\n")

print("\n"*2)
print(" <---   LOCALITZACIÓ DELS ERRORS   ---> \n")

print("-"*50)
for i in range(len(classLabels)):
    if (not i in labels_to_skip):
        if (i == 5 or i == 8 or i == 9):
            print(classLabels[i] + ": \t\t" + str(int(resultsCorrupting[i])))
        else:
            print(classLabels[i] + ": \t" + str(int(resultsCorrupting[i])))
print("-"*50 + "\n")

print("\n"*2)
print(" <---   MATRIU GENERAL DE RESULTATS   ---> \n")

print("-"*100)
print("\t", end='')
for i in range(len(classLabelsCmp)):
    if (not i in labels_to_skip):
        print("\t" + classLabelsCmp[i], end='')
print("")
for i in range(len(classLabels)):
    if (not i in labels_to_skip):
        if (i == 5 or i == 8 or i == 9): print(classLabels[i] + ": \t\t", end='')#"%.2f" % ((resultsCorrect[i]/resultsTotal[i])*100.0), end='')
        else: print(classLabels[i] + ": \t", end='')#"%.2f" % ((resultsCorrect[i]/resultsTotal[i])*100.0), end='')
        for j in range(len(classLabels)):
            if (not j in labels_to_skip):
                print("%.2f" % ((results[i][j]/resultsTotal[i])*100.0), end='')
                print("%\t", end='')
        print("")
print("-"*100 + "\n")
