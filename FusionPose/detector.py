#Made by Arroyo

#Fusion lib
from fusion import TFInference, isCompleteHuman, fromBodyToCoco

#MachineLearning
from sklearn.neural_network import MLPClassifier
from joblib import load

#OpenPose
import sys
import cv2
import os
from sys import platform
import argparse
import time


#tf
sys.path.insert(1, '/home/adria/Documents/Assignatures/Tendencies_en_Robotica/HomeSoundSystem/tfPose/')
from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator, BodyPart
from tf_pose.networks import get_graph_path, model_wh

DEBUG = False

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
    

def detect(data):
    
    query = [[]]
    i = 0
    for d in data.values():
        if i >= 17:
            break
        query[0].append(d.x)
        query[0].append(d.y)
        i+=1
    
    ans = clf.predict(query)
  
    if ans == 1:
        print("USUARIO DE PIE")
    else:
        print("USUARIO EN EL SUELO!")

if __name__ == "__main__":
    
    clf = load('model.joblib') 

    cam = cv2.VideoCapture(2)
    cam.set(cv2.CAP_PROP_BUFFERSIZE,1)

    #Starting OpenPose
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

    while(True):
        ret_val, imageToProcess = cam.read()
        #imageToProcess = cv2.imread("./foto.jpg")

        humans = TFInference(imageToProcess,tfe)
        
        if len(humans) > 1:
            print("More than one human detected TF. Skipping frame.")
            continue

        if len(humans) == 0:
            print("No visible humans")
            continue

        TF_data = humans[0].body_parts

        isCompleteSkeleton = isCompleteHuman(TF_data)
        
        if isCompleteSkeleton:
            print("Found! Detecting using TF result")
            detect(TF_data)
        else:
            print("Not a complete human with TF!.\nTrying with OP...")
            datum = OpenPoseInference(imageToProcess,op)
            OP_data = fromBodyToCoco(datum.poseKeypoints[0],imageToProcess.shape[1],imageToProcess.shape[0])
            isCompleteSkeleton = isCompleteHuman(OP_data)
            
            if isCompleteSkeleton:
                print("Found! Detecting using OpenPose result")
                detect(OP_data)
            else:
                print("Not a complete human with OpenPose!.")
        