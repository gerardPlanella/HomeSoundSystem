# Made by Adria Arroyo Inspired by Miquel Saula & Gerard Planella (Confinament 2020)
# Classifica postures d'un dataset creat amb fusion.py.
# 0 -> usuari al terra
# 1 -> usuari de peu

from collections import Counter

import random 
from sklearn.neural_network import MLPClassifier

from joblib import dump

import random
import datetime
import numpy as np
import math

PERCENTAGE_TESTING = 0.30

def getAsList(fileName):
    
    A = []
    print(fileName + " is being processed...")
    
    line_count = 0
    
    with open(fileName) as f:
        for line in f:
            line_count+=1
            parts = line.split(";")
            poses = []
            #if(fileName == "./old_datasets/stand_adria_first_dataset.dataset" and line_count > 100): return A
            i = 0
            for p in parts:
                chunks = p.split(" ")
                if i >= 17: break 
                if chunks[0] != '\n' and chunks[0] != '':
                    poses.append([chunks[1],chunks[2]])
                    i+=1
            if i != 17:
                print("WARNING: i es " + str(i) + " at file line " + str(line_count))     
            A.append(poses)
    
    return A

if __name__ == '__main__':
    
    A = getAsList("./old_datasets/stand_adria_first_dataset.dataset")
    
    B = []
    for e in A:
        B.append(0)
        
    A_o = A.copy()
    B_o = B.copy()
    
    C = getAsList("./old_datasets/floor_adria_first_dataset.dataset")
    
    D = []
    for e in C:
        D.append(1)


    print("From files, got: B D" + str(len(B)) + " " + str(len(D)))
    #Concatenation
    A += C
    B += D

    #List shuffle.
    for i in range(len(A)-1, 0, -1): 
      
        # Pick a random index from 0 to i  
        j = random.randint(0, i + 1)  
        
        # Swap arr[i] with the element at random index  
        A[i], A[j] = A[j], A[i]  
        B[i], B[j] = B[j], B[i]  



    A_test = []
    B_test = []

    A_train = []
    B_train = []

    for i in range(0, int(len(A))):
        if (i < int(len(A) * PERCENTAGE_TESTING)):
            A_test.append(A[i])
            B_test.append(B[i])
        else:
            A_train.append(A[i])
            B_train.append(B[i])


    a_test = np.asarray(A_test, dtype=np.float32)
    a_train = np.asarray(A_train, dtype=np.float32)
    
    nsamples, nx, ny = a_test.shape
    a_test = a_test.reshape((nsamples,nx*ny))

    nsamples, nx, ny = a_train.shape
    a_train = a_train.reshape((nsamples,nx*ny))

    ref = datetime.datetime.now()

    ALPHA = 1e-5

    print("Train test: " + str(len(a_train)) + " "+ str(len(a_test)) + " Total: " +str(len(a_train)+len(a_test)))

    
    for o in a_test:
        print("A_test pose has " + str(len(o)))

    clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(75, 25, 75), random_state=0, activation='logistic', max_iter=300)
    clf.fit(a_train, B_train)

    timepassed4training = datetime.datetime.now() - ref
    ref = datetime.datetime.now()

    accuracy = 0
    for i in range(len(a_test)):
        feature = a_test[i]
        
        
        index = B_test[i]

        result = clf.predict(np.array(feature).reshape(1, -1))

        if (result[0] == index): accuracy += 1
    
    pepe = Counter(B_test)
    print("COUNT:" + str(pepe))
    
    timepassed = datetime.datetime.now() - ref

    print("-"*50)
    print("Alpha: " + str(ALPHA))
    print("Layer 1: " + str(25) + " - Layer 2: " + str(25))
    print("Layer 3: " + str(True))
    print("Accuracy: " + str(accuracy/len(a_test) * 100.0))
    print("Training time: " + str(timepassed4training.total_seconds()))
    print("Testing time: " + str(timepassed.total_seconds()))

    #dump(clf, 'model.joblib') 
    