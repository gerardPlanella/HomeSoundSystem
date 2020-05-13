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
PERCENTAGE_TESTING = 1
PERCENTAGE_TOTAL = 1
ALPHA = 5e-4

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']

model = 0
with open("modelv5.pkl", 'rb') as file:
    model = pickle.load(file)

path = 'spoonfall.json'
with open(path) as f:
    data = json.load(f)

features_testing = []
index_testing = []

for i in range(0, int(len(data))):
    features_testing.append(data[i]["features_rand"])
    index_testing.append(data[i]["classIndex_rand"])

for i in range(len(features_testing)):
    feature = features_testing[i]
    index = index_testing[i]

    result = np.array(model.predict_proba(np.array(feature).reshape(1, -1))[0])
    print(result)
    print("index: " + classLabels[(np.argmax(result))])
