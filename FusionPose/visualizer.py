from dataset import HumanPositions,Dataset
import cv2
from tf_pose.estimator import TfPoseEstimator, BodyPart
import numpy as np
from tf_pose import common
import time
import sys
import traceback
import argparse

SHOW_KEYS = False

class Visualizer():
    
    def __init__(self,fileNameOut,w,h, datasetName = None, dataset = None):
        self.fileNameOut = fileNameOut

        if dataset is None:
            self.dataset = Dataset(datasetName=datasetName)
        else:
            self.dataset = dataset

        self.w = w
        self.h = h

        self.imageIndex = 0
        self.deletedIndex = 0
        self.listToDelete = []
        self.deletedFrames = False
        self.dontShowData = False
        self.showingIndex = 0
        self.classification = None

        self.textHelper = ["plain data","train data","test data","np train data","np test data"]

        self.draw(self.w,self.h)


    def showDeleteList(self, val):
        self.deletedFrames = val
        if val:
            deletedIndex = 0
            
            self.dontShowData = (len(self.listToDelete) == 0)
            if not self.dontShowData: 
                self.imageIndex = self.listToDelete[0] - 2
        else:
            self.showingIndex = 0
            self.dontShowData = False

        self.draw(self.w,self.h)

    def deleteLine(self):
        dataLine = self.imageIndex + 2
        if dataLine not in self.listToDelete:
            self.listToDelete.append(dataLine)
            print("Line added to the delete list...")
        
    def restorLine(self):
        dataLine = self.imageIndex + 2
        if dataLine in self.listToDelete:
            self.listToDelete.remove(dataLine)
            print("Line removed from the delete list...")
    
    def printDeleteList(self):
        print(self.listToDelete)

    def updateDataAndDraw(self,data,c):
        self.dataset.data = [data]
        self.dataset.classData = [0]
        self.classification = c
        self.draw(self.w,self.h)
        key = cv2.waitKey(250)            

        if key == 27:
            cv2.destroyAllWindows()
            sys.exit(-1)        

    def lastImage(self):
        #Update data.
        
        self.dataset.updateData()

        if self.imageIndex != (len(self.dataset.data) - 1):
            self.imageIndex = len(self.dataset.data) - 1
            self.draw(self.w,self.h)
            print("New data! Updating to new pose!")

    def prevImage(self):
        if self.deletedFrames:
            
            self.dontShowData = (len(self.listToDelete) == 0)
            if not self.dontShowData: 
                self.deletedIndex -= 1
                if self.deletedIndex < 0:
                    self.deletedIndex = len(self.listToDelete) - 1

                self.imageIndex = self.listToDelete[self.deletedIndex] - 2
            
        else:
            self.imageIndex -=1
            if(self.imageIndex < 0):
            #Check depending on the data shown.
                if self.showingIndex == 0:    
                    self.imageIndex = len(self.dataset.data) - 1
                elif self.showingIndex == 1:
                    self.imageIndex = len(self.dataset.trainData) - 1
                elif self.showingIndex == 2:
                    self.imageIndex = len(self.dataset.testData) - 1
                elif self.showingIndex == 3:
                    self.imageIndex = len(self.dataset.npTrainData) - 1
                elif self.showingIndex == 4:
                    self.imageIndex = len(self.dataset.npTestData) - 1
                
        self.draw(self.w,self.h)   
     
    def nextImage(self):
        
        if self.deletedFrames:

            self.dontShowData = (len(self.listToDelete) == 0)
            
            if not self.dontShowData:    
                self.deletedIndex += 1
            
                if self.deletedIndex >= len(self.listToDelete):
                    self.deletedIndex = 0
                
                self.imageIndex = self.listToDelete[self.deletedIndex] - 2
        else:
            self.imageIndex +=1
            #Check depending on the data shown.
            if self.showingIndex == 0:    
                if(self.imageIndex >= len(self.dataset.data)):
                    self.imageIndex = 0
            elif self.showingIndex == 1:
                if(self.imageIndex >= len(self.dataset.trainData)):
                    self.imageIndex = 0
            elif self.showingIndex == 2:
                if(self.imageIndex >= len(self.dataset.testData)):
                    self.imageIndex = 0
            elif self.showingIndex == 3:
                if(self.imageIndex >= len(self.dataset.npTrainData)):
                    self.imageIndex = 0
            elif self.showingIndex == 4:
                if(self.imageIndex >= len(self.dataset.npTestData)):
                    self.imageIndex = 0
        
        self.draw(self.w,self.h)
    
    def deleteSelectedLines(self):
        self.dataset.copyRemovingLines(self.fileNameOut,self.listToDelete)

    def draw(self,w,h):
        img = np.zeros((h,w,3), np.uint8)
    

        #Modify this according to keyboard.
    
        if self.showingIndex == 0:    
            dataset_data = self.dataset.data
            dataset_class = self.dataset.classData

        elif self.showingIndex == 1:
            dataset_data = self.dataset.trainData
            dataset_class = self.dataset.trainClassData
            
        elif self.showingIndex == 2:
            dataset_data = self.dataset.testData
            dataset_class = self.dataset.testClassData

        elif self.showingIndex == 3:
            dataset_data = self.dataset.npTrainData
            dataset_class = self.dataset.npTrainClassData

        elif self.showingIndex == 4:
            dataset_data = self.dataset.npTestData
            dataset_class = self.dataset.npTestClassData
        
        
           
        windowTitle = "Visualizer - Looking at " + str(self.dataset.human_position) + " pose from " + str(self.dataset.fileName)

        if self.dontShowData or len(dataset_data) == 0:
            title = "No data available"
            (nameW,nameH),baseline = cv2.getTextSize(title,cv2.FONT_HERSHEY_SIMPLEX,0.35,thickness=1)
            cv2.putText(img,title, (w//2- nameW//2, h//2 + nameH//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, [20,20,200],thickness=1)
            cv2.destroyAllWindows()
            cv2.imshow(windowTitle, img)
            return

        data = dataset_data[self.imageIndex]

       

        centers = {}
        # draw point
        for i in range(common.CocoPart.Background.value):
            if i not in data.keys():
                continue

            body_part = data[i]
            center = (int(body_part.x * w + 0.5), int(body_part.y * h + 0.5))
            centers[i] = center
            cv2.circle(img, center, 3, common.CocoColors[i], thickness=3, lineType=8, shift=0)
            
                
        # draw line
        for pair_order, pair in enumerate(common.CocoPairsRender):
            if pair[0] not in data.keys() or pair[1] not in data.keys():
                continue

            # npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)
            cv2.line(img, centers[pair[0]], centers[pair[1]], [256,256,256], 3)



        for i in range(common.CocoPart.Background.value):
            if i not in data.keys():
                continue

            center = centers[i]
            
            partName = str(common.CocoPart(i))
            partName = partName.split(".")[1]
            
            (nameW,nameH),baseline = cv2.getTextSize(partName,cv2.FONT_HERSHEY_SIMPLEX,0.35,thickness=1)
            
            if i in [2, 3, 4, 9, 10]:
                #Rigth SIDE
                cv2.putText(img,partName, (center[0] - nameW - 10, center[1] + nameH//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, [0,255,0],thickness=1)
                pass
            elif i in [5, 6, 7, 12, 13]:
                #Left side.
                cv2.putText(img,partName, (center[0] + 10,center[1] + nameH//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, [0,255,0],thickness=1)
            elif i in [0, 1, 8, 11]:
                #Neck, nose and hips.
                cv2.putText(img,partName, (center[0] - nameW//2,center[1] + nameH//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, [0,255,0],thickness=1)
            else:
                #Head
                if i in [15, 17]:
                    cv2.putText(img,partName, (center[0] + 10, center[1] - nameH//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, [0,255,0],thickness=1)
                else:
                    cv2.putText(img,partName, (center[0] - nameW - 10,center[1] - nameH//2), cv2.FONT_HERSHEY_SIMPLEX, 0.35, [0,255,0],thickness=1)
                pass


        #Draw UI data.
        x = 0
        y = 0
        textSize = 0.35
        #Show information
        testShowing = ""
        if self.deletedFrames:
            textShowing = "list of frames to delete"
        else: 
            textShowing = self.textHelper[self.showingIndex]
        
        if self.showingIndex != 0:
            textShowing += " for model " + self.dataset.model.name

        if self.classification is not None:
            y+=self.debugText("Webcam data...",img,x,y,textSize)
        else:
            y+=self.debugText("Showing " + textShowing,img,x,y,textSize)
            y+=self.debugText("Skeleton index is " + str(self.imageIndex),img,x,y,textSize)
            y+=self.debugText("Skeleton class is "+ str(HumanPositions(dataset_class[self.imageIndex])) + " (" + str(dataset_class[self.imageIndex])+")",img,x,y,textSize)
            aux = ""
        
            for e in dataset_data[self.imageIndex].values():
                aux+= "(%d %.2f) " % (e.part_idx, e.score)
            
            self.debugText(aux,img,x,h - 20,0.3)
        
        y+=self.debugText("MPLClassifier output: Human " + str(HumanPositions(self.classification)).lower(),img,10,h - 30,0.5)
    
       
        #Show controls:
        if SHOW_KEYS:
            y = 0
            x = w
            text = ["Press d: Next Image",
            "Press a: Prev Image",
            "Press Space to add the frame to delete list",
            "Press z to restore the frame from delete list",
            "Press p: Print delete list",
            "Press v: Shows delete list",
            "Press *: Creates a new dataset excluding elements from delete list",
            "Press b: Shows plain data list",
            "Press n:    Shows train data list",
            "Press m:     Shows test data list",
            "Press ,: Shows np train data list",
            "Press .:  Shows np test data list"]

            for i in range(0,len(text),1):
                (nameW,nameH),baseline = cv2.getTextSize(text[i],cv2.FONT_HERSHEY_SIMPLEX,textSize,thickness=1)
                cv2.putText(img,text[i], (x - nameW,y + nameH + baseline), cv2.FONT_HERSHEY_SIMPLEX, textSize, [200,20,200],thickness=1)
                y+= nameH + baseline
        
        
        #cv2.destroyAllWindows()
        cv2.imshow(windowTitle, img)
    
    def debugText(self,text,img,x,y,textSize):
        (nameW,nameH),baseline = cv2.getTextSize(text,cv2.FONT_HERSHEY_SIMPLEX,textSize,thickness=1)
        cv2.putText(img,text, (x,y + nameH + baseline), cv2.FONT_HERSHEY_SIMPLEX, textSize, [256,256,256],thickness=1)
        return nameH +baseline

    def showData(self,index):
        self.showingIndex = index
        self.draw(self.w,self.h)

    def startNavigationControls(self):
        try:
            while(True):    
                
                key = cv2.waitKey(0)            

                if key == 27:
                    break 
                
                if key == ord("d"):
                    self.nextImage()
                
                if key == ord("a"):
                    self.prevImage()    

                if key == ord(" "):
                    self.deleteLine()
                
                if key == ord("z"):
                    self.restorLine()

                if key == ord("p"):
                    self.printDeleteList()
                
                if key == ord("v"):
                    self.showDeleteList(True)


                if key == ord("*"):
                    self.deleteSelectedLines()

                if key == ord("b"):
                    self.showDeleteList(False)
                    
                if key == ord("n"):
                    self.showData(1)

                if key == ord("m"):
                    self.showData(2)

                if key == ord(","):
                    self.showData(3)

                if key == ord("."):
                    self.showData(4)
                
        
        except Exception as e:
            print(e)
            traceback.print_exc()
            cv2.destroyAllWindows()
            sys.exit(-1)

    

def modeLookFile(args):

    visual = Visualizer(args.dataset_out,640,480,datasetName=args.dataset_in)
        

    while(True):
        
        visual.lastImage()
        key = cv2.waitKey(250)      
        if key == 27:
            break

def modeNavigate(args):
    try:
        visual = Visualizer(args.dataset_out,640,480,datasetName=args.dataset_in)

        while(True):    
            
            key = cv2.waitKey(0)            

            if key == 27:
                break 
            
            if key == ord("d"):
                visual.nextImage()
            
            if key == ord("a"):
                visual.prevImage()    

            if key == ord(" "):
                visual.deleteLine()
            
            if key == ord("z"):
                visual.restorLine()

            if key == ord("p"):
                visual.printDeleteList()
            
            if key == ord("v"):
                visual.showDeleteList(True)

            if key == ord("b"):
                visual.showDeleteList(False)

            if key == ord("*"):
                visual.deleteSelectedLines()
            
    
    except Exception as e:
        print(e)
        traceback.print_exc()
        cv2.destroyAllWindows()
        sys.exit(-1)

if __name__ == "__main__":

    print("\n\n\n\n\n**********START OF PROGRAM**********\n\n")
    
    parser = argparse.ArgumentParser(description='La pera')
    parser.add_argument('--dataset_in', type=str,required=True)
    parser.add_argument('--look_file', type=bool)
    
    parser.add_argument('--dataset_out', type=str,default="New.",required=False)
    args = parser.parse_args()
                

    if args.dataset_out == "New.":
        args.dataset_out = args.dataset_in + "_generated.dataset"


    if args.look_file is not None and args.look_file:
        modeLookFile(args)
    else:
        modeNavigate(args)