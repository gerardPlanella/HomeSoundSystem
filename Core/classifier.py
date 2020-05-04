from sklearn import neighbors, datasets
from sklearn.neural_network import MLPClassifier
import numpy as np
import math
import pickle

MODEL_PATH = "modelCNN.hdf5"
MODEL_JSON_PATH = "model_CNN.json"

CERTAINTY_DIFFERENCE_THRESHOLD = 0.1#0.302

classLabels = ['Complain', 'FireAlarm', 'BoilingWater', 'GlassBreak', 'Doorbell', 'Fall', 'CutleryFall', 'HeavyBreath', 'Rain', 'Help', 'RunningWater', 'Silence']
#classLabels = ['Bus','Car','CityPark','Classroom','Countryside','Crowd','Factory','Library','Market_pedest','Office','Seaside','Stadium','Station','Traffic','Train']

class Classifier():
    __slots__= ['model', 'ok']

    def __init__(self):
        try:
            self.model = load_trained_model(MODEL_JSON_PATH, MODEL_PATH)
            ok = True
        except:
            ok = False

    def load_trained_model(JSON_path, weights_path):
        json_file = open(JSON_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        model.load_weights(weights_path)
        return model

    def predict(self, components):
        result = np.array(self.model.predict(np.array(components).reshape(1, 40, 13, 1))[0])

        index = np.argmax(result)
        confidence = result[index]

        #result = np.delete(result, index)
        #confidence_2 = max(result)

        if((confidence) < CERTAINTY_DIFFERENCE_THRESHOLD):
            index = -1
            event = ""
            print("Packet received but discarded")
        else:
            event = classLabels[index]

        return[event, index, confidence]
