from enum import Enum
from model import Model
from tf_pose import common
from tf_pose.estimator import BodyPart
import os
import random 
from collections import Counter
import sys
import numpy as np
from os import listdir
from os.path import isfile, join

class HumanPositions(Enum):
    STANDING = 0
    SITTING = 1
    ON_THE_FLOOR = 2
    
    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return HumanPositions[s]
        except KeyError:
            print("Key was " + str(s))
            raise ValueError()

class Dataset():
    def __init__(self, datasetName = None, folderName = None, human_position = None, data = None):
        


        self.model = None

        if data is not None:
            self.human_position = HumanPositions.STANDING
            self.datasetName = "RealTime!"
            self.fileName = "RealTime!"
            self.data = data

            pass
        else:

            if folderName is not None:
                onlyfiles = [f for f in listdir(folderName) if isfile(join(folderName, f))]
                if len(onlyfiles) != 0:
                    datasetName = (folderName+onlyfiles[0])
                else:
                    print("Empty folder!")
                    sys.exit(-1)
            
            self.path,self.fileName = os.path.split(os.path.abspath(datasetName))
            
            #Add or remove dynamically the .dataset.
            if self.fileName.endswith(".dataset"):
                self.datasetName = self.fileName[:-8]
            else:
                self.datasetName = self.fileName    

            #Set filename to the file
            self.fileName = datasetName

            if human_position is not None:
                self.human_position = human_position
                self.data = []
                if not os.path.isfile(self.fileName):
                    with open(self.fileName, "a+") as f:
                        f.write(str(human_position.value) + "\n")
            else:
                self.human_position, self.data = self.readFile(self.fileName,True)

        self.classData = []

        for e in self.data:
            self.classData.append(self.human_position.value)
             
        self.appendedDatasetNames = []

        self.percentage = 30
        
        self.testData         = []
        self.testClassData    = []
        self.trainData        = []
        self.trainClassData   = []

        self.npTrainData      = []
        self.npTrainClassData = []

        self.npTestClassData  = []
        self.npTestData       = []

        if folderName is not None:
            self.appendDatasetsFromFolder(folderName)

    def __str__(self):

        return ("\nDataset \""+str(self.datasetName)+"\": \n\tDataset name: " + str(self.datasetName) + "\n" +
        "\tFilename: " + str(self.fileName) + "\n" +
        "\tDatasets appended: " + str(self.appendedDatasetNames) + "\n" +
        "\tPath: " + str(self.path) + "\n" +
        "\tTesting percentage: " + str(self.percentage) + "\n" +
        self.getStringVal("Plain Data",self.data,self.classData) +
        self.getStringVal("Train Data",self.trainData,self.trainClassData) +
        self.getStringVal("Test Data",self.testData,self.testClassData) + 
        self.getStringVal("NP Train Data", self.npTrainData,self.npTrainClassData) +
        self.getStringVal("NP Test Data", self.npTestData,self.npTestClassData))


    def printNP(self):
        print(self.getStringVal("NP Train Data", self.npTrainData,self.npTrainClassData) +
        self.getStringVal("NP Test Data", self.npTestData,self.npTestClassData))

    def getStringVal(self,title,data,classData):
                
        differentClassesAre = set(classData)
        nSkeletonsData = Counter(classData)
        return ("\t"+title+":\n"+
        "\t\tData size: " + str(len(data)) + "\n" +
        "\t\tDifferent classes in data: " + str(differentClassesAre) + "\n" +
        "\t\tNumber of skeletons of class 0: " + str(nSkeletonsData[0]) + "\n" +
        "\t\tNumber of skeletons of class 1: " + str(nSkeletonsData[1]) + "\n" +
        "\t\tNumber of skeletons of class 2: " + str(nSkeletonsData[2]) + "\n")

    def updateData(self):
        self.human_position, self.data = self.readFile(self.fileName,False)


    def appendDatasetsFromFolder(self,folderName):
        onlyfiles = [f for f in listdir(folderName) if isfile(join(folderName, f))]
        
        for dataFile in onlyfiles:
            completeName = (folderName + dataFile)
            if completeName != self.fileName:
                self.appendDataset(datasetName=(completeName))

    def datasetTestingPercentage(self, percentage):
        print("Setting new dataset test percentage to %.2f" %(percentage,))
        self.percentage = percentage
        self.createTestAndTrainData()

    def shuffleDataAndClass(self, data, dataClass):
        for i in range(len(data) - 1, 0, -1): 
        
            # Pick a random index from 0 to i  
            j = random.randint(0, i)  

            # Swap arr[i] with the element at random index  
            data[i], data[j] = data[j], data[i]  
            dataClass[i], dataClass[j] = dataClass[j], dataClass[i]  

    def extractDataType(self,objective_class,data,dataClass,maxElementsAccepted):
        l = len(data)
        aux = []
        auxClass = []
        itemsAdded = 0
        for i in range(0, l, 1):
            #Per a totes les poses.
            if dataClass[i] == objective_class:
                aux.append(data[i])
                auxClass.append(objective_class)   
                itemsAdded+=1
                if itemsAdded >= maxElementsAccepted:
                    break
        return aux,auxClass
    
    def createTestAndTrainData(self):
        
        #Extract subgroups
        minElements = min((Counter(self.classData)).values())
         
        data_copy_group = [[],[],[]]
        class_copy_group = [[],[],[]]
        
        for i in range(0,3,1):
            data_copy_group[i], class_copy_group[i] = self.extractDataType(i, self.data, self.classData, minElements)

        #Shuffle subgroups
        for i in range(0,3,1):
            self.shuffleDataAndClass(data_copy_group[i], class_copy_group[i])

        #Auxilar variables
        auxDiv = (self.percentage/100)
        
        self.testData = []
        self.testClassData = []
        self.trainData = []
        self.trainClassData = []
        
        for i in range(0,3,1):
            self.testData       += data_copy_group[i][:int(len(data_copy_group[i]) * auxDiv)]
            self.testClassData  += class_copy_group[i][:int(len(class_copy_group[i])*auxDiv)] 
    
            self.trainData      += data_copy_group[i][int(len(data_copy_group[i]) * auxDiv):]
            self.trainClassData += class_copy_group[i][int(len(class_copy_group[i])*auxDiv):]

    
        print("Resulting lists have %d skeletons in test data and %d skeletons in training data" % (len(self.testData),len(self.trainData)))


    def adaptDataToModel(self,model):
        
        newData = []
        newClass = []
        i = 0
        for pose in self.data:
            
            #Check if its a valid skeleton    
            if model.checkSkeleton(pose):
                #Valid pose.
                newData.append(pose)
                newClass.append(self.classData[i])
                
            i+=1

        self.model = model
        self.data = newData
        self.classData = newClass
        
        print("Dataset Updated acording to model.") 

    def fromBodyPartToMLP (self, model, dataIn, dataClassIn, dataOut, dataClassOut):
        poseIndex = 0
        
        modelLen = len(model.skeleton_points)

        for pose in dataIn:
            aux = []
                    
            elementIndex = 0
            
            for e in pose.values():
                if elementIndex >= modelLen:
                    break
                
                aux.append(float(e.x))
                aux.append(float(e.y))

                elementIndex += 1

            dataOut.append(aux)
            dataClassOut.append(dataClassIn[poseIndex])
        
            poseIndex+=1

    def genDatForModel(self, model):
        #Note: This could be optimized by creating np data before splitting into train and test.

        print("Generating model " + model.name)
        self.npTrainData      = []
        self.npTrainClassData = []

        self.npTestClassData  = []
        self.npTestData       = []
        
        self.fromBodyPartToMLP(model, self.trainData,self.trainClassData,self.npTrainData,self.npTrainClassData)
        self.npTrainData = np.array(self.npTrainData, dtype=np.float32)

        self.fromBodyPartToMLP(model, self.testData,self.testClassData,self.npTestData,self.npTestClassData)
        self.npTestData = np.array(self.npTestData, dtype=np.float32)
        
        print("From train data, extracted " + str(len(self.npTrainClassData)) + " out of " + str(len(self.trainClassData)) + " skeletons")
        print("From test data, extracted " + str(len(self.npTestClassData)) + " out of " + str(len(self.testClassData)) + " skeletons")


    def appendDataset(self, datasetName = None, dataset = None):
        
        newDataset = None
        
        if dataset is not None:
            print("\nAppending dataset \"" + str(dataset.datasetName) + "\"")
            newDataset = dataset
        elif datasetName is not None:
            print("\nAppending dataset \"" + datasetName + "\"")
            newDataset = Dataset(datasetName=datasetName)
        
        self.appendedDatasetNames.append(newDataset.datasetName)
        self.data += newDataset.data
        self.classData += newDataset.classData
    
    """
    Copies the dataset into a new file.
        Args: 
            fileNameOut: name of the new file
            listToDelete: a list with the lines that will NOT be copied
    """
    def copyRemovingLines(self,fileNameOut,listToDelete):
        with open(self.fileName,"r") as f:
            lines = f.readlines() 

        print("File had " + str(len(lines)) + " lines.")

        index = 1
        #TODO: OPTIMIZE THIS TO ONLY 1 FILE WRITE. Use a buffer...
        with open(fileNameOut, "w+") as f:
            while(index < len(lines)):

                if index not in listToDelete:
                    f.write(lines[index-1])
                else:
                    print("Not saving file line " + str(index))
                index+=1
        print("New file has " + str(index-2) + " lines.")

    def appendDataToFile(self, data):

        print("Appending data: " + str(data))
        
        result = ""
        
        for d in data.values():
            result += str(d.part_idx) + " " + str(d.x) + " " + str(d.y) + " " + str(d.score) + ";"
        
        result += "\n"

        print("Appending data to " + self.fileName + ". Data lenght: " + str(len(data)))
        
        with open(self.fileName, "a+") as f:
            f.write(result)
    
    def readFile(self,fileName, verbose):
        
        A = []
        if verbose:
            print("Loading " + fileName + "...",end='')
        
        line_count = 0
        poseType = -1

        with open(fileName,"r") as f:
            for line in f:
                line_count+=1
                if(line_count == 1):
                    poseType = HumanPositions(int(line[0]))
                    continue
                    
                parts = line.split(";")
                pose = {}
                
                i = 0
                for p in parts:

                    chunks = p.split(" ")

                    if chunks[0] != '\n' and chunks[0] != '':
                        partIndex = int(chunks[0])
                        pose.update({partIndex: BodyPart(0,partIndex,float(chunks[1]),float(chunks[2]),float(chunks[3]))})
                        i+=1
                
                A.append(pose)
        if verbose:
            print(" OK! Loaded " + str(line_count-1) + " skeletons")
        return (poseType,A)
