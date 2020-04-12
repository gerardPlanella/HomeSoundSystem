#Made by Gerard Planella / Miquel Saula

from sklearn import neighbors, datasets
from sklearn.neural_network import MLPClassifier
import json
import random
import datetime
import numpy as np
import math
"""
######      CODE FOR KNN        #######

TOTAL_K_TO_TEST = 10
PERCENTAGE_TESTING = 0.25
PERCENTAGE_TOTAL = 0.05
n_neighbors = 3

with open('components.json') as f:
    data = json.load(f)

features_training = []
index_training = []

features_testing = []
index_testing = []

for i in range(0, int(len(data) * PERCENTAGE_TOTAL)):
    if (i < int(len(data) * PERCENTAGE_TESTING * PERCENTAGE_TOTAL)):
        features_testing.append(data[i]["features_rand"])
        index_testing.append(data[i]["classIndex_rand"])
    else:
        features_training.append(data[i]["features_rand"])
        index_training.append(data[i]["classIndex_rand"])

ref = datetime.datetime.now()

for k in range(1, TOTAL_K_TO_TEST):
    ref = datetime.datetime.now()

    results = {
        "uniform": [],
        "distance": []
    }

    for weights in ['uniform', 'distance']:
        clf = neighbors.KNeighborsClassifier(k, weights=weights, algorithm = "kd_tree", n_jobs = 10 )
        clf.fit(features_training, index_training)

        for i in range(0, len(features_testing)):
            results[weights].append(clf.predict([features_testing[i]]))
            #print(i)


    accuracy = {"uniform" :  0, "distance":  0}
    correct = {"uniform" :  0, "distance":  0}
    total = {"uniform" :  len(results["uniform"]), "distance":  len(results["distance"])}

    #print("Rest set: "  + str(index_testing) + "\n\n")
    #print("Results + " + str(results) + "\n\n")

    for weights in ['uniform', 'distance']:
        for i in range(0, len(results[weights])):
            if results[weights][i] == index_testing[i]:
                correct[weights] = correct[weights] + 1
    for weights in ['uniform', 'distance']:
        accuracy[weights] = float(float(correct[weights]) / float(total[weights]))

    timepassed = datetime.datetime.now() - ref
    print("-"*30 + "\nK VALUE: " + str(k) + "\nTime spent: " + str(timepassed.total_seconds()) + "\nAccuracy : \n\tUniform = " + str(accuracy["uniform"]) + ", \n\tDistance =  " + str(accuracy["distance"]) + "\n" + "-"*30)
"""

TOTAL_K_TO_TEST = 10
PERCENTAGE_TESTING = 0.30
PERCENTAGE_TOTAL = 1
ALPHA = 5e-4

with open('components_v2.json') as f:
    data = json.load(f)

features_training = []
index_training = []

features_testing = []
index_testing = []

for i in range(0, int(len(data) * PERCENTAGE_TOTAL)):
    if (i < int(len(data) * PERCENTAGE_TESTING * PERCENTAGE_TOTAL)):
        features_testing.append(data[i]["features_rand"])
        index_testing.append(data[i]["classIndex_rand"])
    else:
        features_training.append(data[i]["features_rand"])
        index_training.append(data[i]["classIndex_rand"])

ref = datetime.datetime.now()

for third in range(2):
    for n1 in range(1, 5):
        for n2 in range(1, 5):
            for i in range(3): 
                solvr = 'solvr'
                ref = datetime.datetime.now()

                ALPHA = 1e-5 * (math.pow(10, i))

                if (third == 0): clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(25 * n1, 25 * n2), random_state=None, activation='logistic')
                else: clf = MLPClassifier(solver='adam', alpha=ALPHA, hidden_layer_sizes=(25 * n1, 25 * n2, 75), random_state=None, activation='logistic')
                clf.fit(features_training, index_training)

                timepassed4training = datetime.datetime.now() - ref
                ref = datetime.datetime.now()

                accuracy = 0
                for i in range(len(features_testing)):
                    feature = features_testing[i]
                    index = index_testing[i]

                    result = clf.predict(np.array(feature).reshape(1, -1))
                    if (result[0] == index): accuracy += 1

                timepassed = datetime.datetime.now() - ref

                print("-"*50)
                print("Alpha: " + str(ALPHA))
                print("Layer 1: " + str(n1*25) + " - Layer 2: " + str(n2*25))
                print("Layer 3: " + str(third == 1))
                print("Accuracy: " + str(accuracy/len(features_testing) * 100.0))
                print("Training time: " + str(timepassed4training.total_seconds()))
                print("Testing time: " + str(timepassed.total_seconds()))


"""
BEST CONFIGURATION FOUND TO DATE:

--------------------------------------------------

<BEST IN NEW DATASET>
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 75
Layer 3: True
Accuracy: 86.18343195266273
Training time: 27.017637
Testing time: 0.483985
--------------------------------------------------


Alpha: 0.0001
Solver: 'adam'
Layer 1: 75 - Layer 2: 75
Layer 3: False
Accuracy: 92.57383966244726
Training time: 27.031665
Testing time: 0.696889
--------------------------------------------------
"""

"""
RESULTS FROM COMPLETE TEST (Allof them uses adam):
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 25
Layer 3: False
Accuracy: 90.45007032348803
Training time: 13.598248
Testing time: 0.679423
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 25
Layer 3: False
Accuracy: 90.61884669479606
Training time: 13.440776
Testing time: 0.711589
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 25
Layer 3: False
Accuracy: 90.32348804500702
Training time: 13.350827
Testing time: 0.707409
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 50
Layer 3: False
Accuracy: 90.9001406469761
Training time: 16.197745
Testing time: 0.662254
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 50
Layer 3: False
Accuracy: 90.9985935302391
Training time: 14.440071
Testing time: 0.663613
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 50
Layer 3: False
Accuracy: 90.73136427566807
Training time: 15.108359
Testing time: 0.661869
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 75
Layer 3: False
Accuracy: 91.12517580872012
Training time: 19.192205
Testing time: 0.677549
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 75
Layer 3: False
Accuracy: 91.27988748241913
Training time: 20.208435
Testing time: 0.677661
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 75
Layer 3: False
Accuracy: 90.81575246132209
Training time: 18.279024
Testing time: 0.675621
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 100
Layer 3: False
Accuracy: 91.46272855133614
Training time: 23.24098
Testing time: 0.681374
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 100
Layer 3: False
Accuracy: 91.25175808720113
Training time: 19.470285
Testing time: 0.682456
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 100
Layer 3: False
Accuracy: 90.8720112517581
Training time: 21.092094
Testing time: 0.680576
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 25
Layer 3: False
Accuracy: 90.71729957805907
Training time: 15.974296
Testing time: 0.664183
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 25
Layer 3: False
Accuracy: 90.9001406469761
Training time: 14.719971
Testing time: 0.671272
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 25
Layer 3: False
Accuracy: 90.042194092827
Training time: 11.900431
Testing time: 0.661901
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 50
Layer 3: False
Accuracy: 91.35021097046413
Training time: 16.114787
Testing time: 0.673476
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 50
Layer 3: False
Accuracy: 92.0534458509142
Training time: 20.769761
Testing time: 0.696708
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 50
Layer 3: False
Accuracy: 91.15330520393812
Training time: 19.95788
Testing time: 0.849946
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 75
Layer 3: False
Accuracy: 92.09563994374122
Training time: 27.148543
Testing time: 0.793394
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 75
Layer 3: False
Accuracy: 91.70182841068917
Training time: 22.397726
Testing time: 0.689959
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 75
Layer 3: False
Accuracy: 90.98452883263009
Training time: 17.447771
Testing time: 0.69909
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 100
Layer 3: False
Accuracy: 91.71589310829818
Training time: 26.988089
Testing time: 0.851715
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 100
Layer 3: False
Accuracy: 91.57524613220815
Training time: 24.575906
Testing time: 0.770284
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 100
Layer 3: False
Accuracy: 90.63291139240506
Training time: 20.300591
Testing time: 0.880362
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 25
Layer 3: False
Accuracy: 90.85794655414908
Training time: 16.977744
Testing time: 0.699166
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 25
Layer 3: False
Accuracy: 91.54711673699015
Training time: 22.458192
Testing time: 1.277294
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 25
Layer 3: False
Accuracy: 90.74542897327707
Training time: 16.106553
Testing time: 0.738388
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 50
Layer 3: False
Accuracy: 91.67369901547117
Training time: 28.124252
Testing time: 0.847658
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 50
Layer 3: False
Accuracy: 91.72995780590718
Training time: 25.939131
Testing time: 1.160392
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 50
Layer 3: False
Accuracy: 91.72995780590718
Training time: 21.349973
Testing time: 0.682609
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 75
Layer 3: False
Accuracy: 92.57383966244726
Training time: 27.031665
Testing time: 0.696889
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 75
Layer 3: False
Accuracy: 92.13783403656821
Training time: 22.518706
Testing time: 0.698769
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 75
Layer 3: False
Accuracy: 91.57524613220815
Training time: 20.957442
Testing time: 0.691636
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 100
Layer 3: False
Accuracy: 92.39099859353024
Training time: 25.760025
Testing time: 0.703525
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 100
Layer 3: False
Accuracy: 92.46132208157525
Training time: 28.78256
Testing time: 0.702618
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 100
Layer 3: False
Accuracy: 91.74402250351618
Training time: 24.904911
Testing time: 0.720068
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 25
Layer 3: False
Accuracy: 91.53305203938116
Training time: 22.120859
Testing time: 0.686311
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 25
Layer 3: False
Accuracy: 91.72995780590718
Training time: 22.064107
Testing time: 0.677241
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 25
Layer 3: False
Accuracy: 91.12517580872012
Training time: 19.693117
Testing time: 0.687375
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 50
Layer 3: False
Accuracy: 91.67369901547117
Training time: 19.963536
Testing time: 0.687327
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 50
Layer 3: False
Accuracy: 92.40506329113924
Training time: 25.818398
Testing time: 0.695132
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 50
Layer 3: False
Accuracy: 91.33614627285513
Training time: 19.155518
Testing time: 0.693629
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 75
Layer 3: False
Accuracy: 92.12376933895922
Training time: 23.434286
Testing time: 0.711609
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 75
Layer 3: False
Accuracy: 91.08298171589311
Training time: 15.712302
Testing time: 0.699084
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 75
Layer 3: False
Accuracy: 91.27988748241913
Training time: 17.092611
Testing time: 0.704716
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 100
Layer 3: False
Accuracy: 91.9690576652602
Training time: 27.3758
Testing time: 0.82923
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 100
Layer 3: False
Accuracy: 92.22222222222223
Training time: 26.676576
Testing time: 0.800925
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 100
Layer 3: False
Accuracy: 90.8720112517581
Training time: 17.919538
Testing time: 0.801291
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 25
Layer 3: True
Accuracy: 90.37974683544304
Training time: 19.807562
Testing time: 0.750059
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 25
Layer 3: True
Accuracy: 90.0
Training time: 19.635928
Testing time: 0.778545
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 25
Layer 3: True
Accuracy: 88.88888888888889
Training time: 17.140804
Testing time: 0.781239
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 50
Layer 3: True
Accuracy: 90.9423347398031
Training time: 25.088921
Testing time: 0.747241
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 50
Layer 3: True
Accuracy: 89.0154711673699
Training time: 20.012004
Testing time: 0.77781
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 50
Layer 3: True
Accuracy: 89.0576652601969
Training time: 21.389013
Testing time: 0.747296
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 75
Layer 3: True
Accuracy: 91.23769338959212
Training time: 28.145099
Testing time: 0.753943
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 75
Layer 3: True
Accuracy: 90.80168776371308
Training time: 26.31315
Testing time: 0.755453
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 75
Layer 3: True
Accuracy: 89.957805907173
Training time: 25.788065
Testing time: 0.762527
--------------------------------------------------
Alpha: 0.0001
Layer 1: 25 - Layer 2: 100
Layer 3: True
Accuracy: 90.82981715893108
Training time: 31.430922
Testing time: 0.764592
--------------------------------------------------
Alpha: 0.001
Layer 1: 25 - Layer 2: 100
Layer 3: True
Accuracy: 89.71870604781998
Training time: 21.969392
Testing time: 0.811139
--------------------------------------------------
Alpha: 0.01
Layer 1: 25 - Layer 2: 100
Layer 3: True
Accuracy: 89.12798874824192
Training time: 24.289037
Testing time: 0.771922
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 25
Layer 3: True
Accuracy: 90.91420534458508
Training time: 22.04446
Testing time: 0.725393
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 25
Layer 3: True
Accuracy: 91.11111111111111
Training time: 19.762453
Testing time: 0.737328
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 25
Layer 3: True
Accuracy: 89.28270042194093
Training time: 15.280657
Testing time: 0.729894
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 50
Layer 3: True
Accuracy: 90.61884669479606
Training time: 20.603171
Testing time: 0.747519
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 50
Layer 3: True
Accuracy: 91.20956399437412
Training time: 22.267815
Testing time: 0.761791
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 50
Layer 3: True
Accuracy: 91.27988748241913
Training time: 27.82128
Testing time: 0.790706
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 75
Layer 3: True
Accuracy: 91.60337552742615
Training time: 27.141422
Testing time: 0.773023
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 75
Layer 3: True
Accuracy: 91.56118143459916
Training time: 31.011918
Testing time: 0.768142
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 75
Layer 3: True
Accuracy: 90.92827004219409
Training time: 28.251797
Testing time: 0.772129
--------------------------------------------------
Alpha: 0.0001
Layer 1: 50 - Layer 2: 100
Layer 3: True
Accuracy: 90.54852320675106
Training time: 21.466184
Testing time: 1.164838
--------------------------------------------------
Alpha: 0.001
Layer 1: 50 - Layer 2: 100
Layer 3: True
Accuracy: 91.47679324894514
Training time: 31.969692
Testing time: 0.875882
--------------------------------------------------
Alpha: 0.01
Layer 1: 50 - Layer 2: 100
Layer 3: True
Accuracy: 91.49085794655414
Training time: 38.55922
Testing time: 0.769774
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 25
Layer 3: True
Accuracy: 90.28129395218004
Training time: 18.713657
Testing time: 0.76084
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 25
Layer 3: True
Accuracy: 90.9985935302391
Training time: 25.205793
Testing time: 0.747862
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 25
Layer 3: True
Accuracy: 90.59071729957806
Training time: 19.082541
Testing time: 0.748877
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 50
Layer 3: True
Accuracy: 91.25175808720113
Training time: 25.055277
Testing time: 0.763039
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 50
Layer 3: True
Accuracy: 91.39240506329114
Training time: 26.691937
Testing time: 0.78907
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 50
Layer 3: True
Accuracy: 90.63291139240506
Training time: 24.325244
Testing time: 0.769503
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 75
Layer 3: True
Accuracy: 91.53305203938116
Training time: 24.465797
Testing time: 0.784755
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 75
Layer 3: True
Accuracy: 91.91279887482419
Training time: 30.438157
Testing time: 0.771521
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 75
Layer 3: True
Accuracy: 90.63291139240506
Training time: 22.249378
Testing time: 0.815205
--------------------------------------------------
Alpha: 0.0001
Layer 1: 75 - Layer 2: 100
Layer 3: True
Accuracy: 91.84247538677918
Training time: 33.964071
Testing time: 0.78946
--------------------------------------------------
Alpha: 0.001
Layer 1: 75 - Layer 2: 100
Layer 3: True
Accuracy: 92.46132208157525
Training time: 39.167116
Testing time: 0.783499
--------------------------------------------------
Alpha: 0.01
Layer 1: 75 - Layer 2: 100
Layer 3: True
Accuracy: 91.65963431786217
Training time: 34.340014
Testing time: 0.786882
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 25
Layer 3: True
Accuracy: 91.58931082981717
Training time: 24.542525
Testing time: 0.755188
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 25
Layer 3: True
Accuracy: 91.08298171589311
Training time: 24.270501
Testing time: 0.759302
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 25
Layer 3: True
Accuracy: 90.60478199718706
Training time: 25.294426
Testing time: 0.764474
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 50
Layer 3: True
Accuracy: 91.16736990154712
Training time: 21.123666
Testing time: 0.764056
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 50
Layer 3: True
Accuracy: 90.18284106891701
Training time: 21.921784
Testing time: 0.840683
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 50
Layer 3: True
Accuracy: 90.52039381153305
Training time: 19.336321
Testing time: 0.766376
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 75
Layer 3: True
Accuracy: 91.51898734177215
Training time: 25.685202
Testing time: 0.788045
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 75
Layer 3: True
Accuracy: 91.63150492264415
Training time: 28.893339
Testing time: 1.004931
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 75
Layer 3: True
Accuracy: 91.05485232067511
Training time: 32.325822
Testing time: 1.011165
--------------------------------------------------
Alpha: 0.0001
Layer 1: 100 - Layer 2: 100
Layer 3: True
Accuracy: 92.09563994374122
Training time: 32.052675
Testing time: 0.885393
--------------------------------------------------
Alpha: 0.001
Layer 1: 100 - Layer 2: 100
Layer 3: True
Accuracy: 91.43459915611814
Training time: 28.998718
Testing time: 0.941876
--------------------------------------------------
Alpha: 0.01
Layer 1: 100 - Layer 2: 100
Layer 3: True
Accuracy: 91.36427566807313
Training time: 30.053437
Testing time: 0.885475
"""
