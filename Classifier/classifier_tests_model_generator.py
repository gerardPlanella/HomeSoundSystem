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

for nfile in range(3):
    path = 'components_100_50.json'
    if (nfile == 1): path = 'components_250_125.json'
    elif (nfile == 2): path = 'components_500_250.json'

    with open(path) as f:
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

    model = MLPClassifier(solver='adam', alpha=1e-4, hidden_layer_sizes=(100, 100, 75), random_state=None, activation='logistic')
    model.fit(features_training, index_training)

    path2 = 'model_100.pkl'
    if (nfile == 1): path2 = 'model_250.pkl'
    elif (nfile == 2): path2 = 'model_500.pkl'
    with open(path2, 'wb') as file:
        pickle.dump(model, file)
