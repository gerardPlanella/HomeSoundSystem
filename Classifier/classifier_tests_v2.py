#Made by Gerard Planella / Miquel Saula

from sklearn import neighbors, datasets
from sklearn.neural_network import MLPClassifier
import json
import random
import datetime
import numpy as np
import math
import pickle

TOTAL_K_TO_TEST = 10
PERCENTAGE_TESTING = 0.30
PERCENTAGE_TOTAL = 1
ALPHA = 5e-4

#classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']
classLabels = ['Bus','Car','CityPark','Classroom','Countryside','Crowd','Factory','Library','Market_pedest','Office','Seaside','Stadium','Station','Traffic','Train']

def normalize(data):
    maxv = 0
    index = 0
    for i in range(len(data)):
        v = data[i]
        if maxv < v:
            maxv = v
            index = i

    scale_factor = MAX_VALUE / maxv
    for i in range(len(data)):
        data[i] = data[i]*scale_factor

    return data

with open('componentsv4.json') as f:
    data = json.load(f)

features_training = []
index_training = []

features_testing = []
index_testing = []

for i in range(0, int(len(data) * PERCENTAGE_TOTAL)):
    if (i < int(len(data) * PERCENTAGE_TESTING * PERCENTAGE_TOTAL)):
        features_testing.append(data[i]["features_rand"])
        index_testing.append(data[i]["classIndex_rand"])
    else:
        features_training.append(data[i]["features_rand"])
        index_training.append(data[i]["classIndex_rand"])

ref = datetime.datetime.now()

model = 0
best_model = model
best_accuracy = 0

for third in range(2):
    for n1 in range(1, 5):
        for n2 in range(1, 5):
            for i in range(3):
                solvr = 'solvr'
                ref = datetime.datetime.now()

                ALPHA = 1e-5 * (math.pow(10, i))

                if (third == 0): clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(25 * n1, 25 * n2), random_state=None, activation='logistic')
                else: clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(25 * n1, 25 * n2, 75), random_state=None, activation='logistic')
                clf.fit(features_training, index_training)

                if (ALPHA == 1e-3 and third == 1 and n1 == 4 and n2 == 3):
                    model = clf

                timepassed4training = datetime.datetime.now() - ref
                ref = datetime.datetime.now()

                accuracy_true = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                n_total = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                accuracy = 0
                for i in range(len(features_testing)):
                    feature = features_testing[i]
                    index = index_testing[i]

                    result = clf.predict(np.array(feature).reshape(1, -1))
                    n_total[result[0]] += 1
                    if (result[0] == index):
                        accuracy_true[result[0]] += 1
                        accuracy += 1

                if (accuracy > best_accuracy):
                    timepassed = datetime.datetime.now() - ref

                    best_accuracy = accuracy
                    best_model = model

                    print("-"*50)
                    print("Alpha: " + str(ALPHA))
                    print("Layer 1: " + str(n1*25) + " - Layer 2: " + str(n2*25))
                    print("Layer 3: " + str(third == 1))

                    print("Total accuracy: " + str(accuracy/len(features_testing) * 100.0))
                    print("Accuracies: ")
                    for i in range(len(accuracy_true)):
                        print("\t" + classLabels[i] + ": \t" + str(accuracy_true[i]/n_total[i]*100.0))

                    print("Training time: " + str(timepassed4training.total_seconds()))
                    print("Testing time: " + str(timepassed.total_seconds()))


path = "modelv4.pkl"
with open(path, 'wb') as file:
    pickle.dump(best_model, file)
