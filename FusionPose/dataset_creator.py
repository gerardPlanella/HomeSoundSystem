"""
Creates a dataset from a folder if specified.
Creates a dataset from camera if no folder is defined.
"""

#Show inference times.
DEBUG = False

#Only work with a single image
SINGLE_IMAGE = False
SINGLE_IMAGE_PATH = "/home/adria/Documents/Assignatures/Tendencies_en_Robotica/HomeSoundSystem/FusionPose/images/Standing.jpg"

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

if __name__ == '__main__':    
    
    parser = argparse.ArgumentParser(description='La pera')
    parser.add_argument('--cameraIndex', type=int, default=2)
    parser.add_argument('--folder', type=str,default="NOFOLDER")
    parser.add_argument('--datasetName', type=str, default="dataset_default.dataset")

    parser.add_argument('--human_position', type=lambda human_position: HumanPositions[human_position], choices=list(HumanPositions),required=True)

    args = parser.parse_args()
    
    usingFolder = (args.folder != "NOFOLDER")

    if usingFolder:
        
        filenames = glob.glob(args.folder + "/*.jpg")
    
        if not SINGLE_IMAGE:
            t = time.time()
            images = [cv2.resize(cv2.imread(img),(640,480),interpolation=cv2.INTER_AREA) for img in filenames]
            elapsed = time.time() - t        
        else:
            images = []
        
        if len(images) == 0:
            print("No images loaded. Exiting...")
            if not SINGLE_IMAGE:
                sys.exit(0)
        
    else:
        cam = cv2.VideoCapture(args.cameraIndex)
        cam.set(cv2.CAP_PROP_BUFFERSIZE,1)
        
    imageIndex = 0
    
    dataset = Dataset(args.datasetName, args.human_position)


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
        if usingFolder and not SINGLE_IMAGE:
            print("Loaded " + str(len(images)) + " images! Time loading: %.4f" % (elapsed))
        
        while(True):
            if not SINGLE_IMAGE:
                if args.folder == "NOFOLDER":
                    ret_val, imageToProcess = cam.read()
                else:
                    imageToProcess = images[imageIndex]
            else:
                imageToProcess = cv2.imread(SINGLE_IMAGE_PATH)
            
            humans = TFInference(imageToProcess,tfe)
            
            #Check is tf detected more than one human
            if len(humans) > 1:
                print("More than one human detected TF. Skipping frame.")

                imageIndex+=1
                if usingFolder:
                    print("File name was" + str(filenames[imageIndex-1]))
                    if(imageIndex >= len(images)):
                        print("We are done with the folder.")
                        break
                continue
            
            isCompleteSkeleton = False

            #Check if tf detected any human part
            if len(humans) == 0:
                print("No visible humans.")
                if usingFolder:
                    print("Problematic file name" + str(filenames[imageIndex]))
                #continue
            else:

                #Tf detected something, save it
                TF_data = humans[0].body_parts
                
                dataReliable = dataset.isScoreAcceptable(TF_data)
                
                if not dataReliable:
                    print("TF data not reliable in this frame. Data is " + str(TF_data))
                    if usingFolder:
                        print("Problematic file name" + str(filenames[imageIndex]))

                #Check if the data is usable for all models.
                isCompleteSkeleton = (Model.FULL_BODY().checkSkeleton(TF_data) and dataReliable)
            
            if isCompleteSkeleton:
                #We are good only with TF.
                dataset.appendDataToFile(TF_data)
            else:
                #Proceed with OpenPose...
                datum = OpenPoseInference(imageToProcess,op)
                
                if(len(datum.poseKeypoints.shape) == 3):
                
                    #Convert from BODY 25 TO COCO
                    OP_data = Model.fromBodyToCoco(datum.poseKeypoints[0],imageToProcess.shape[1],imageToProcess.shape[0])
                    
                    #Check if the TF skeleton data is usable for any model.
                    worthItToSave = dataset.skeletonFitsAModel(OP_data)
                    if worthItToSave:
                        dataset.appendDataToFile(OP_data)
                    else:    
                        print("Cant detect anything usable with OP. Discarting frame " + str(imageIndex) + "!")
                        if usingFolder:
                            print("Problematic file name" + str(filenames[imageIndex]))
                        print("Data detected was " + str(OP_data))
                        
                else:
                    print("OpenPose didnt detect anything.")
                    if usingFolder:
                            print("Problematic file name" + str(filenames[imageIndex]))
            
            imageIndex+=1
            if usingFolder:
                if(imageIndex >= len(images)):
                    print("We are done with the folder.")
                    break
            
            if SINGLE_IMAGE:
                break

    except Exception as e:
        traceback.print_exc()
        print(e)
        sys.exit(-1)