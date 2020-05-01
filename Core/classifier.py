from sklearn import neighbors, datasets
from sklearn.neural_network import MLPClassifier
import numpy as np
import math
import pickle

MODEL_PATH = "modelv6.pkl"

CERTAINTY_DIFFERENCE_THRESHOLD = 0.5

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']
#classLabels = ['Bus','Car','CityPark','Classroom','Countryside','Crowd','Factory','Library','Market_pedest','Office','Seaside','Stadium','Station','Traffic','Train']

class Classifier():
    __slots__= ['model', 'ok']

    def __init__(self):
        try:
            with open(MODEL_PATH, 'rb') as file:
                self.model = pickle.load(file)
            ok = True
        except:
            ok = False

    def predict(self, components):
        result = np.array(self.model.predict_proba(np.array(components).reshape(1, -1))[0])

        index = np.argmax(result)
        confidence = result[index]

        result = np.delete(result, index)
        confidence_2 = max(result)

        if((confidence - confidence_2) < CERTAINTY_DIFFERENCE_THRESHOLD):
            index = -1
            event = ""
            print(".", end='')
        else:
            event = classLabels[index]

        return[event, index, confidence]
