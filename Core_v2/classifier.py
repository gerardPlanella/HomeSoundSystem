from sklearn import neighbors, datasets
from sklearn.neural_network import MLPClassifier
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, Conv2D, MaxPooling2D, GlobalAveragePooling2D
from keras.layers import Convolution1D, Conv1D, MaxPooling1D, GlobalAveragePooling1D
from keras.optimizers import Adam
from keras.utils import np_utils
from keras import backend as K
from sklearn import metrics
import math
import json
import random
import datetime
import numpy as np
import math
import keras
from keras.models import model_from_json

MODEL_PATH = "modelCNN.hdf5"
MODEL_JSON_PATH = "model_CNN.json"

CERTAINTY_DIFFERENCE_THRESHOLD = 0.6

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']

def load_trained_model(JSON_path, weights_path):
    json_file = open(JSON_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)

    model.load_weights(weights_path)
    return model

class Classifier():
    __slots__= ['model', 'ok']

    def __init__(self, model):
        self.model = model
        try:
            self.model = self.load_trained_model(MODEL_JSON_PATH, MODEL_PATH)
            ok = True
        except:
            ok = False

    def predict(self, components):
        result = np.array(self.model.predict(components))[0]
        print(result)

        index = np.argmax(result)
        confidence = result[index]

        #result = np.delete(result, index)
        #confidence_2 = max(result)

        if((confidence) < CERTAINTY_DIFFERENCE_THRESHOLD):
            print("Packet received but discarded [" + classLabels[index] + "]")
            index = -1
            event = ""
        else:
            event = classLabels[index]

        return[event, index, confidence]
