import sys
import numpy as np
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.metrics import average_precision_score
from random import randint
import pickle
import matplotlib.pyplot as plt
import random
from sklearn import calibration 
############################################
dataset = sys.argv[1]
cur_dir = sys.argv[1]
num_class = int(sys.argv[2])

###################      read HMM features from file   ###############################
def readFeaturesFromHMMFile (file):
    featureList = list()
    try:
        with open(file) as f:
            content = f.readlines()
        for item in content:
            data = item.strip().split("\t")
            data = data[: -1];      data = [(float(i)) for i in data]
            featureList.append(np.array(data))
    except FileNotFoundError:
        print(file)
    # print(len(featureList))
    return np.array(featureList)
########### read BLAST features from file  ##################
def readFeaturesFromBlastFile (file, target):
    featureList1 = list(); featureList2 = list()
    targetIdx = (target)
    try:
        with open(file) as f:
            content = f.readlines()
        
        for item in content:
            data = item.strip().split("\t")
            data = [(float(i)) for i in data]
            data = np.array(data)
            # remove Identity and get 2 feature from each family
            data1 = np.delete(data, np.s_[2::3], 0)
            
            # get only 3 feature corresponding to that family
            st = targetIdx*3;      en = st + 3
            data2 = data[st:en]

            featureList1.append(data1);      featureList2.append(data2)

    except FileNotFoundError:
        print(file)
    return np.array(featureList1), np.array(featureList2)



###############    get blast feature, get hmm feature, merge them and return   ###########
def getMergedFeatureTN(target, famList):

    flag = 1; lbl = 0
    for i in famList:

        if i == target:
            continue
        blast = cur_dir+"/features/train_blast/CLASS_"+str(i)+"_blastFeatures.txt"
        hmm = cur_dir+"/features/train_phmm/CLASS_"+str(i)+"_phmmFeatures.txt"

        featureData_hmm = readFeaturesFromHMMFile(hmm)
        featureData_blast1, featureData_blast2 = readFeaturesFromBlastFile(blast, target)
        # print(featureData_hmm.shape, featureData_blast1.shape)
        total_sz = len(featureData_blast1)
        data_sz = 10 if total_sz >10 else total_sz

        if flag == 1:
            # HMM + BLAST 1074*2 features merged
            train_all_feat1 = np.concatenate((featureData_hmm[ : data_sz], featureData_blast1[ : data_sz]), axis = 1)
            # HMM + BLAST only 3 features merged
            train_all_feat2 = np.concatenate((featureData_hmm[ : data_sz], featureData_blast2[ : data_sz]), axis = 1)
            # BLAST only 3 features
            train_all_feat3 = featureData_blast2[ : data_sz]
            # labels for all
            train_labels = np.full(data_sz, lbl)
            flag = 0
        else:
            # HMM + BLAST 1074*2 features merged
            temp1 = np.concatenate((featureData_hmm[: data_sz], featureData_blast1[: data_sz]), axis = 1)
            train_all_feat1 = np.concatenate((train_all_feat1, temp1), axis = 0)
            # HMM + BLAST only 3 features merged
            temp2 = np.concatenate((featureData_hmm[: data_sz], featureData_blast2[: data_sz]), axis = 1)
            train_all_feat2 = np.concatenate((train_all_feat2, temp2), axis = 0)
            # BLAST only 3 features
            train_all_feat3 = np.concatenate((train_all_feat3, featureData_blast2[: data_sz]), axis = 0)
            # labels for all
            temp_lbl = np.full(data_sz, lbl)
            train_labels = np.concatenate((train_labels, temp_lbl), axis = 0)

    return train_all_feat1, train_all_feat2, train_all_feat3, train_labels

def getMergedFeatureTP(target, famList):

    lbl = 1
   
    blast = cur_dir"/features/train_blast/CLASS_"+str(target)+"_blastFeatures.txt"
    hmm = cur_dir"/features/train_phmm/CLASS_"+str(target)+"_phmmFeatures.txt"

    featureData_hmm = readFeaturesFromHMMFile(hmm)
    featureData_blast1, featureData_blast2 = readFeaturesFromBlastFile(blast, target, flag=1) ### change this value to 1/0 for v2 / v1
    # print(len(featureData_blast1), len(featureData_hmm))
    data_sz = min(len(featureData_blast1), len(featureData_hmm))

    # HMM + BLAST 1074*2 features merged
    train_all_feat1 = np.concatenate((featureData_hmm[:data_sz], featureData_blast1[:data_sz]), axis = 1)
    # HMM + BLAST only 3 features merged
    train_all_feat2 = np.concatenate((featureData_hmm[:data_sz], featureData_blast2[:data_sz]), axis = 1)
    # BLAST only 3 features
    train_all_feat3 = featureData_blast2[:data_sz]
    # labels for all
    train_labels = np.full(data_sz, lbl)
    # print(train_all_feat1.shape, featureData_hmm.shape)

    return train_all_feat1, train_all_feat2, train_all_feat3, train_labels

def trainSVM(train_all_feat, train_labels, modelNo):

    clf_blast = svm.LinearSVC(class_weight={0:0.1, 1:0.9}, penalty='l1', loss='squared_hinge', dual=False, tol=1e-3, max_iter=10000)

    clf_blast.fit(train_all_feat, train_labels)
    sc = clf_blast.score(train_all_feat, train_labels)
    # print("Model %d\t%f" % (modelNo, sc) )
    modelName = cur_dir+"/models/CLASS_"+str(target)+"_model1_"+ str(modelNo) +".sav"
    pickle.dump(clf_blast, open(modelName, 'wb'))

#########################################################################################################




##################   train with merged feature   ###################


famList = np.arange(0,num_class)

# start = int(sys.argv[3])
# end = int(sys.argv[4])


for target in famList:
# for target in idxList:
    # print("#####################   CLASS_%d   ######################" %( target) )
    
    train_all_feat1, train_all_feat2, train_all_feat3, train_labels = getMergedFeatureTP(target, famList)
    # print(train_all_feat1.shape, train_all_feat2.shape, train_all_feat3.shape, train_labels.shape)
    train_tn_feat1, train_tn_feat2, train_tn_feat3, train_tn_labels = getMergedFeatureTN(target, famList)

    # HMM + BLAST 1074*2 features
    train_all_feat1 = np.concatenate((train_all_feat1, train_tn_feat1), axis = 0)
    # HMM + BLAST only 3 features
    train_all_feat2 = np.concatenate((train_all_feat2, train_tn_feat2), axis = 0)
    # BLAST only 3 features
    train_all_feat3 = np.concatenate((train_all_feat3, train_tn_feat3), axis = 0)

    # labels for all
    train_labels = np.concatenate((train_labels, train_tn_labels), axis = 0)

    # print(train_all_feat1.shape, train_all_feat2.shape, train_all_feat3.shape, train_labels.shape)

    # Model 1 --->  HMM + BLAST 1074*2 features    
    trainSVM(train_all_feat1, train_labels, 1)
    # Model 2 --->  HMM + BLAST only 3 features    
    trainSVM(train_all_feat2, train_labels, 2)
    # Model 3 --->  BLAST only 3 features    
    trainSVM(train_all_feat3, train_labels, 3)
    
    