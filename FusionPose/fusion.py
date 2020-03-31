#OpenPose
import sys
import cv2
import os
from sys import platform
import argparse
import time


#tf
from tf_pose import common
import cv2
import numpy as np
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import argparse
import logging

#tf init



try:
    # Import Openpose Ubuntu
    try:

	    sys.path.append('/usr/local/python')
	    from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    # Program Arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="/home/adria/Pictures/Webcam/d.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()
    
    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = "./models/"
    params["net_resolution"] = "320x176"
    params["number_people_max"] = "1"
    params["render_pose"] = "0"
    
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Process Image
    datum = op.Datum()
    imageToProcess = cv2.imread(args[0].image_path)
   
	#Add image to datum
    datum.cvInputData = imageToProcess
    t = time.time()
    
    #OpenPose Inference
    opWrapper.emplaceAndPop([datum])
    elapsed = time.time() - t
    print('OPENPOSE done in %.4f seconds.\n' % (elapsed))
    
    #Save and close OpenPose
    ImageOpenPose = datum.cvOutputData
    opWrapper.stop()
    
    w = 656
    h = 368

    e = TfPoseEstimator(get_graph_path("cmu"), target_size=(432, 368))

    t = time.time()
    
    #TF Inference
    humans = e.inference(imageToProcess, resize_to_default=(w > 0 and h > 0), upsample_size=4.0)
    elapsed = time.time() - t
    
    print('TF done in %.4f seconds.\n' % (elapsed))
    
    ImageTF = TfPoseEstimator.draw_humans(imageToProcess, humans, imgcopy=True)

    a = humans[0].body_parts[0]
    image_h, image_w = imageToProcess.shape[:2]
    
    print('%s x,y (%.2f, %.2f) score=%.2f' % (a.get_part_name(), a.x * image_w + 0.5, a.y * image_h + 0.5, a.score))

    #Resize de les imatges resultants.        
    #ImageOpenPose = cv2.resize(ImageOpenPose, (0, 0), None, .5, .5)
    #ImageTF = cv2.resize(ImageTF, (0, 0), None, .5, .5)
    
    #result = np.hstack((ImageOpenPose, ImageTF))
	# Display Image
    print("Body keypoints: \n" + str(datum.poseKeypoints[0]))
    #cv2.imshow("FusionPose", result)
    #cv2.waitKey(0)
    
except Exception as e:
    print(e)
    sys.exit(-1)