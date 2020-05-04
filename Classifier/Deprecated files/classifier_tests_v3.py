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
MAX_VALUE = 1.0

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']
#classLabels = ['Bus','Car','CityPark','Classroom','Countryside','Crowd','Factory','Library','Market_pedest','Office','Seaside','Stadium','Station','Traffic','Train']

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

with open('componentsv4.json') as f:
    data = json.load(f)

features_training = []
index_training = []

features_testing = []
index_testing = []

for i in range(0, int(len(data) * PERCENTAGE_TOTAL)):
    if (i < int(len(data) * PERCENTAGE_TESTING * PERCENTAGE_TOTAL)):
        features_testing.append(normalize(data[i]["features_rand"]))
        index_testing.append(data[i]["classIndex_rand"])
    else:
        features_training.append(normalize(data[i]["features_rand"]))
        index_training.append(data[i]["classIndex_rand"])

ref = datetime.datetime.now()

model = 0
best_model = model
best_accuracy = 0

for alpha_factor in range(10):
    for n1 in range(1, 10):
        for n2 in range(0, 10):
            for n3 in range(0, 10):
                solvr = 'solvr'
                ref = datetime.datetime.now()

                i = alpha_factor
                exp = alpha_factor/2
                ALPHA = 1e-6 * (math.pow(10, exp)) * (1 + 4*(i%2))

                if (n2 != 0 and n3 != 0): model = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(20 * n1, 20 * n2, 20 * n3), random_state=None, activation='logistic')
                elif (n2 == 0 and n3 != 0): model = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(20 * n1, 20 * n3), random_state=None, activation='logistic')
                elif (n2 != 0 and n3 == 0): model = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(20 * n1, 20 * n2), random_state=None, activation='logistic')
                elif (n2 == 0 and n3 == 0): model = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(20 * n1), random_state=None, activation='logistic')
                model.fit(features_training, index_training)

                timepassed4training = datetime.datetime.now() - ref
                ref = datetime.datetime.now()

                accuracy_true = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                n_total = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                accuracy = 0
                for i in range(len(features_testing)):
                    feature = features_testing[i]
                    index = index_testing[i]

                    result = model.predict(np.array(feature).reshape(1, -1))
                    n_total[result[0]] += 1
                    if (result[0] == index):
                        accuracy_true[result[0]] += 1
                        accuracy += 1

                timepassed = datetime.datetime.now() - ref
                if (accuracy > best_accuracy):
                    best_accuracy = accuracy
                    best_model = model

                    print("Alpha: " + str(ALPHA))
                    print("Layer 1: " + str(n1*20) + " - Layer 2: " + str(n2*20) + " - Layer 3: " + str(n3*20))

                    print("Total accuracy: " + str(accuracy/len(features_testing) * 100.0))
                    print("Accuracies: ")
                    for i in range(len(accuracy_true)):
                        if (i == 5 or i == 8 or i == 9): print("\t" + classLabels[i] + ": \t\t" + str(accuracy_true[i]/n_total[i]*100.0))
                        else: print("\t" + classLabels[i] + ": \t" + str(accuracy_true[i]/n_total[i]*100.0))

                    print("Training time: " + str(timepassed4training.total_seconds()))
                    print("Testing time: " + str(timepassed.total_seconds()))
                    print("-"*50)
                else:
                    print("Training time for failed configuration: " + str(timepassed4training.total_seconds()))


path = "modelv4.pkl"
with open(path, 'wb') as file:
    pickle.dump(best_model, file)
