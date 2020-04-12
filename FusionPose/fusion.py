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



#Classification of poses.

DEBUG = False
OnTheFloor = True


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


def fromBodyToCoco(keypoints,img_w, img_h):
    result = {}
    i = 0
    for p in keypoints:
        if i == 8:
            i=i+1
            continue
        if i >= 19:
            break

        if p[2] != 0:
            if i > 8:
                obj = BodyPart(0,i-1,p[0]/img_w,p[1]/img_h,p[2])
                result.update({i-1:obj})
            else:
                obj = BodyPart(0,i,p[0]/img_w,p[1]/img_h,p[2])
                result.update({i:obj})
        i=i+1
    return result



def isReliableData(poseData):
    for p in poseData.values():
        if p.score < 0.5:
            return False
    return True

def isCompleteHuman(poseData):
    try:
        k = len(poseData)
        if k == 0:
            return False

        if  k < 18:
            for i in range(k):

                if i >= 14:
                    return True

                if i not in poseData:
                    return False
        else:
            return True    

    except Exception as identifier:
        print("EXCEPTION!")
    

def saveData(data):
    
    if OnTheFloor:
        filename = "floor.txt"
    else:
        filename = "stand.txt"
    
    result = ""
    
    for d in data.values():
        result += str(d.part_idx) + " " + str(d.x) + " " + str(d.y) + " " + str(d.score) + "; "
    
    result += "\n"

    print("Saving: " + result)
    """
    f = open(filename, "a+")
    f.write(result)
    f.close()
    """


def OP_draw_humans(npimg, data):
    image_h, image_w = npimg.shape[:2]
    centers = {}
    
    # draw point
    for i in range(common.CocoPart.Background.value):
        if i not in data.keys():
            continue

        body_part = data[i]
        center = (int(body_part.x * image_w + 0.5), int(body_part.y * image_h + 0.5))
        centers[i] = center
        cv2.circle(npimg, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)

    # draw line
    for pair_order, pair in enumerate(common.CocoPairsRender):
        if pair[0] not in data.keys() or pair[1] not in data.keys():
            continue

        # npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
        cv2.line(npimg, centers[pair[0]], centers[pair[1]], [255,0,0], 3)

    return npimg


if __name__ == '__main__':
    

    try:
        cam = cv2.VideoCapture(2)

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

        # Read image
        #imageToProcess = cv2.imread(args[0].image_path)

        #Calculate with OpenPose
        #datum = OpenPoseInference(imageToProcess)
        
        #Calculate with TF.
        #humans = TFInference(imageToProcess, tfe)
    

        while(True):
            ret_val, imageToProcess = cam.read()
            """humans = TFInference(imageToProcess,tfe)
            
            if len(humans) > 1:
                print("More than one human detected TF. Skipping frame.")
                continue
    
            if len(humans) == 0:
                print("No visible humans")
                continue


            TF_data = humans[0].body_parts
            #print(str(time.time())+" TF: "+str(humans[0].body_parts))


            isCompleteSkeleton = isCompleteHuman(TF_data)
            """
            isCompleteSkeleton = False
            if isCompleteSkeleton:
                print("\TF: " + str(TF_data))
                saveData(TF_data)
            else:
                print("Not a complete human with TF!.")
                datum = OpenPoseInference(imageToProcess,op)
                OP_data = fromBodyToCoco(datum.poseKeypoints[0],imageToProcess.shape[1],imageToProcess.shape[0])
                isCompleteSkeleton = isCompleteHuman(OP_data)
                
                if isCompleteSkeleton:
                    print("Saving OP data")
                    saveData(OP_data)
                else:
                    print("Not a complete human with OpenPose!.")


            #if len(humans[0].body_parts)
            #print(str(time.time())+" TF: "+str(humans[0].body_parts))
        

            if DEBUG:

                ImageTF = TfPoseEstimator.draw_humans(imageToProcess, humans, imgcopy=False)
                ImageTF = OP_draw_humans(imageToProcess, OP_data)

                #Resize de les imatges resultants.        
                #ImageOpenPose = cv2.resize(datum.cvOutputData, (0, 0), None, .5, .5)
                #ImageTF = cv2.resize(ImageTF, (0, 0), None, .5, .5)        
                #result = np.hstack((ImageOpenPose, ImageTF))
                # Display Image
                aux = cv2.resize(ImageTF, (0, 0), None, .75, .75)
                cv2.imshow("FusionPose", aux)
                
                if cv2.waitKey(1) == 27:
                    break                

        cv2.destroyAllWindows()

    except Exception as e:
        print(e)
        cv2.destroyAllWindows()
        sys.exit(-1)