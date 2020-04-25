
    #To train all from a folder:
    #python3 model_trainer.py --append_dataset_folder ./all_datasets/ --all True

    
    #To train only one model:
    #

from dataset import Dataset
from model import Model,ModelEnum
import argparse
from sklearn.neural_network import MLPClassifier
from joblib import dump
import random
import datetime
import numpy as np
from visualizer import Visualizer
from joblib import dump
from collections import Counter
import math

#Specifies the percentage of testing samples over the total of skeletons.
RELATION_TESTING_TRAINING = 25

def compute_one_model(args):
    dataset = Dataset(folderName=args.append_dataset_folder)
    
    #Set 30% of the dataset data to test. other 70 to traning.
    
    percentage = RELATION_TESTING_TRAINING
    transformDataset(dataset,percentage,args.model_enum)
    trainAndSaveModel(dataset,args.model_enum)
    #lookForBestTraining(dataset,args.model_enum)

def compute_all_models(args):
        
 
    #Set 30% of the dataset data to test. other 70 to traning.
    percentage = RELATION_TESTING_TRAINING
    
    for enumModel in ModelEnum:
        dataset = Dataset(folderName=args.append_dataset_folder)
        transformDataset(dataset,percentage,enumModel)
        lookForBestTraining(dataset,enumModel)

def transformDataset(dataset, percentage, enumModel):
    if enumModel == ModelEnum.FULL_BODY:
        dataset.adaptDataToModel(Model.FULL_BODY())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.FULL_BODY())
        
    elif enumModel == ModelEnum.FULL_BODY_NO_EARS:
        dataset.adaptDataToModel(Model.FULL_BODY_NO_EARS())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.FULL_BODY_NO_EARS())
        
    elif enumModel == ModelEnum.LEFT_SIDE:
        dataset.adaptDataToModel(Model.LEFT_SIDE())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.LEFT_SIDE())
        
    elif enumModel == ModelEnum.RIGHT_SIDE:
        dataset.adaptDataToModel(Model.RIGHT_SIDE())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.RIGHT_SIDE())
        
    elif enumModel == ModelEnum.TORSO:
        dataset.adaptDataToModel(Model.TORSO())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.TORSO())
        
    elif enumModel == ModelEnum.FULL_TORSO_LEGS:
        dataset.adaptDataToModel(Model.FULL_TORSO_LEGS())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.FULL_TORSO_LEGS())
        
    elif enumModel == ModelEnum.LEFT_TORSO_LEGS:
        dataset.adaptDataToModel(Model.LEFT_TORSO_LEGS())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.LEFT_TORSO_LEGS())
            
    elif enumModel == ModelEnum.RIGHT_TORSO_LEGS:
        dataset.adaptDataToModel(Model.RIGHT_TORSO_LEGS())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.RIGHT_TORSO_LEGS())

    elif enumModel == ModelEnum.TEST_ADRIA:
        dataset.adaptDataToModel(Model.TEST_ADRIA())
        dataset.datasetTestingPercentage(percentage)
        dataset.genDatForModel(Model.TEST_ADRIA())
    else:
        print("Error!"*50)
    
def trainAndSaveModel(dataset,model_enum):
    print(dataset)
    ref = datetime.datetime.now()

    ALPHA = 1e-5
    
    print("About to train with shape: " + str(dataset.npTrainData.shape[0]))
    print(dataset.npTrainData[0])
    print(dataset.npTrainClassData[0])
    clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(75, 25, 75), random_state=0, activation='logistic', max_iter=1000,)
    clf.fit(dataset.npTrainData, dataset.npTrainClassData)
    
    timepassed4training = datetime.datetime.now() - ref
    ref = datetime.datetime.now()

    if dataset.percentage != 0:
        predictions = []
        accuracy = 0
        for i in range(len(dataset.npTestData)):
            feature = dataset.npTestData[i]
        
            index = dataset.npTestClassData[i]

            result = clf.predict(np.array(feature).reshape(1, -1))
            predictions.append(result[0])
            
            if (result[0] == index): accuracy += 1

        timepassed = datetime.datetime.now() - ref
        ak = Counter(predictions)
        print("Counter of predictions " + str(ak))

    
    print(model_enum)
    print("Alpha: " + str(ALPHA))
    print("Layer 1: " + str(25) + " - Layer 2: " + str(25))
    print("Layer 3: " + str(True))
    
    if dataset.percentage != 0:
        print("Accuracy: " + str(accuracy/len(dataset.npTestData) * 100.0))
    
    print("Training time: " + str(timepassed4training.total_seconds()))
    
    if dataset.percentage != 0:
        print("Testing time: " + str(timepassed.total_seconds()))
    print("*"*100)
    #dump(clf, str(model_enum) + ".joblib") 


def lookForBestTraining(dataset, model_enum):
    maxim = 0
    n1c = 0
    n2c = 0
    thirdc = False
    alphac = 0
    mm = None

    for third in range(2):
        for n1 in range(1, 5):
            for n2 in range(1, 5):
                for i in range(3): 
        
                    ALPHA = 1e-5 * (math.pow(10, i))

                    if (third == 0): clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(25 * n1, 25 * n2), random_state=None, activation='logistic', max_iter=1000)
                    else: clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(25 * n1, 25 * n2, 75), random_state=None, activation='logistic', max_iter=1000)
               
                    clf.fit(dataset.npTrainData, dataset.npTrainClassData)
                    
                    accuracy = 0
                    for i in range(len(dataset.npTestData)):
                        feature = dataset.npTestData[i]
                    
                        index = dataset.npTestClassData[i]

                        result = clf.predict(np.array(feature).reshape(1, -1))
                        
                        if (result[0] == index): accuracy += 1

                    acc = accuracy/len(dataset.npTestData) * 100.0

                    if maxim <= acc:

                        maxim = acc
                        n1c = n1
                        n2c = n2c
                        third = thirdc
                        alphac = ALPHA
                        mm = clf
                        if acc == 100:                   
                            print("Alpha: " + str(alphac))
                            print("Layer 1: " + str(n1c * 25) + " - Layer 2: " + str(n2c*25))
                            print("Layer 3: " + str(thirdc == 1))
                            print("Accuracy: " + str(maxim))    
                            print("*"*100)
                            dump(mm, "./magic/auto_" + str(model_enum) + ".joblib") 
                            return

    
    print("Alpha: " + str(alphac))
    print("Layer 1: " + str(n1c * 25) + " - Layer 2: " + str(n2c*25))
    print("Layer 3: " + str(thirdc == 1))
    print("Accuracy: " + str(maxim))    
    print("*"*100)
    dump(mm, "./magic/auto_" + str(model_enum) + ".joblib") 

if __name__ == "__main__":
    
    print("\n\n\n\n\n**********START OF PROGRAM**********\n\n")

    parser = argparse.ArgumentParser(description='La pera')
    parser.add_argument('--dataset_in', type=str)
    parser.add_argument('--append_dataset_folder', type=str)
    parser.add_argument('--model_enum', type=lambda model_enum: ModelEnum[model_enum], choices=list(ModelEnum))
    parser.add_argument('--model_out', type=str,default="model.",required=False)
    parser.add_argument('--all',type=bool,default=False)
    args = parser.parse_args()

    if args.all:
        compute_all_models(args)
    else:
        compute_one_model(args)
    
    #visual = Visualizer("OutFile",1000,900,dataset=dataset)
    #visual.startNavigationControls()
    




    #DEUBG

    #python3 model_trainer.py --dataset_in dataset_default0.dataset 
    #dataset.appendDataset(datasetName="dataset_default1.dataset")
    #dataset.appendDataset(datasetName="dataset_default2.dataset")

    #python3 model_trainer.py --dataset_in ./revised_datasets/gaetan_floor.dataset
    #dataset.appendDataset(datasetName="./revised_datasets/floor_adria_first_dataset.dataset")
    #dataset.appendDataset(datasetName="./revised_datasets/stand_adria_first_dataset.dataset")
    #dataset.appendDataset(datasetName="./revised_datasets/gaetan_sitting.dataset")