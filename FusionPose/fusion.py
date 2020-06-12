"""
Takes an image from the webcam, outputs the following classification: 
Standing - Sitting - OnTheFloor
"""

#Show inference times.
DEBUG = False

#OpenPose deps
import sys
import cv2
import os
from sys import platform
import argparse
import time
import glob

#tf deps
sys.path.insert(1, '/home/adria/Documents/Assignatures/Tendencies_en_Robotica/HomeSoundSystem/tfPose/')
from tf_pose import common
import cv2
import numpy as np

from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh

from model import Model
from dataset import Dataset, HumanPositions

import traceback
from joblib import load
from os import listdir
from os.path import isfile, join
from collections import Counter
from visualizer import Visualizer

def OpenPoseInference(imageToProcess,op):
    #Add image to datum
    datum = op.Datum()
    datum.cvInputData = imageToProcess  

    if DEBUG:
        t = time.time()
    
    #OpenPose Inference
    opWrapper.emplaceAndPop([datum])
    if DEBUG:
        elapsed = time.time() - t
        print('OPENPOSE inference done in %.4f seconds.\n' % (elapsed))
    
    #Save and close OpenPose
    return datum
    

def TFInference(imageToProcess, e):

    if DEBUG:
        t = time.time()
    
    #TF Inference
    humans = e.inference(imageToProcess, resize_to_default=True, upsample_size=4.0)
    if DEBUG:
        elapsed = time.time() - t
        print('TF done in %.4f seconds.\n' % (elapsed))
        
    return humans


def loadAllModelsFromFolder(folderName):
    res = []
    onlyfiles = [f for f in listdir(folderName) if isfile(join(folderName, f))]
    for mo in onlyfiles:
        if mo == "auto_FULL_BODY.joblib":
            model = Model.FULL_BODY()
        elif mo == "auto_FULL_BODY_NO_EARS.joblib":
            model = Model.FULL_BODY_NO_EARS()  
        elif mo == "auto_LEFT_SIDE.joblib":
            model = Model.LEFT_SIDE()
        elif mo == "auto_RIGHT_SIDE.joblib":
            model = Model.RIGHT_SIDE()
        elif mo == "auto_TORSO.joblib":
            model = Model.TORSO()
        elif mo == "auto_FULL_TORSO_LEGS.joblib":
            model = Model.FULL_TORSO_LEGS()
        elif mo == "auto_LEFT_TORSO_LEGS.joblib":
            model = Model.LEFT_TORSO_LEGS()
        elif mo == "auto_RIGHT_TORSO_LEGS.joblib":
             model = Model.RIGHT_TORSO_LEGS()
        elif mo == "auto_TEST_ADRIA.joblib":
             model = Model.TEST_ADRIA()
        else:
            print("FILE READ NOT RECOGNIZED!")
            sys.exit(-1)

        res.append((model,load(folderName + mo)))
    return res

def fromBodyPartToMLP (skeleton, model):
    
    modelLen = len(model.skeleton_points)        
    elementIndex = 0
    aux = [[]]

    for e in skeleton.values():
        if elementIndex >= modelLen:
            break
    
        aux[0].append(float(e.x))
        aux[0].append(float(e.y))
        elementIndex += 1

    return np.array(aux[0]).reshape(1, -1)

def classify(clfs, skeleton):
    results = []
    ke = False
    print("Classify!")
    for clf in clfs:
        if clf[0].checkSkeleton(skeleton):
            #clf[1] contains the trained NN for classifying the clf[0] model
          
            feature = fromBodyPartToMLP(skeleton,clf[0])
            result = clf[1].predict(feature)
            results.append((clf[0],result[0]))
            print("Classify result: " + clf[0].name + " " + str(HumanPositions(result[0])))
            #if(clf[0].name == "RIGHT_SIDE"):return result[0]
            ke = True


    if not ke:
        print("Cant classify, not enough data!")

    return extractFinalClassificationValue(results)

def extractFinalClassificationValue(classificationOutput):
    aux = []

    for resultTuple in classificationOutput:
        aux.append(resultTuple[1])
    
    ResultCounter = Counter(aux)
    pp = max((ResultCounter).values())
    classificationFinalResult = -1

    for resultKey in ResultCounter.keys():
        if ResultCounter[resultKey] == pp:
            classificationFinalResult = resultKey
            break
    
    print("CLASSIFICATION IS " + str(HumanPositions(classificationFinalResult)))
    return classificationFinalResult

if __name__ == '__main__':    
    
    parser = argparse.ArgumentParser(description='La pera')
    parser.add_argument('--camera_index', type=int, default=2)
    
    args = parser.parse_args()
    
    cam = cv2.VideoCapture(args.camera_index)
    cam.set(cv2.CAP_PROP_BUFFERSIZE,1)

    try:

        os.environ['GLOG_minloglevel'] = '50'
        # Import Openpose Ubuntu
        try:

            sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e
        
        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "/home/adria/Documents/Assignatures/Tendencies_en_Robotica/HomeSoundSystem/FusionPose/models/"
        params["model_pose"] = "BODY_25" #MPI_4_layers"
        params["net_resolution"] = "320x176"
        params["number_people_max"] = "1"
        params["render_pose"] = "0"
        params["logging_level"] = "255"

        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start() 

        #Starting TF.
        tfe = TfPoseEstimator(get_graph_path("mobilenet_thin"), target_size=(432,368))
        
        #dataset = Dataset()
        
        dset = Dataset(data=[])
        v = Visualizer("OUT_REALTIME", 640, 480, dataset=dset)
        
        clfs = loadAllModelsFromFolder("./MPL_models/")
        
        while(True):
            ret_val, imageToProcess = cam.read()
            humans = TFInference(imageToProcess,tfe)
            
            #Check is tf detected more than one human
            if len(humans) > 1:
                print("More than one human detected TF. Skipping frame.")
                continue
            
            #Check if tf detected any human part
            if len(humans) == 0:
                print("No visible humans.")
                enoughData = False
                dataReliable = False
                #continue
            else:
                #Tf detected something, save it
                TF_data = humans[0].body_parts
                    
                #Check if the data is usable for all models.
                
                dataReliable = Model.isScoreAcceptable(TF_data,0.3)

                enoughData = Model.skeletonFitsAModel(TF_data)

            if enoughData and dataReliable:
                result = classify(clfs,TF_data)
                
                v.updateDataAndDraw(TF_data, result)
                
            else:    
                print("\t\tCant detect anything usable with TF.")
        
                #Proceed with OpenPose...
                datum = OpenPoseInference(imageToProcess,op)
                
                if(len(datum.poseKeypoints.shape) == 3):
                
                    #Convert from BODY 25 TO COCO
                    OP_data = Model.fromBodyToCoco(datum.poseKeypoints[0],imageToProcess.shape[1],imageToProcess.shape[0])
                    
                    #Check if the TF skeleton data is usable for any model.
                    worthItToSave = Model.skeletonFitsAModel(OP_data)

                    if worthItToSave:
                        result = classify(clfs, OP_data)
                        
                        v.updateDataAndDraw(OP_data, result)
                    else:    
                        print("\t\tCant detect anything usable with OP.")
            
    except Exception as e:
        traceback.print_exc()
        print(e)
        sys.exit(-1)