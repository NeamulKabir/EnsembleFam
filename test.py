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
##########################################
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
    return np.array(featureList)
########### read BLAST features from file  ##################
def readFeaturesFromBlastFile (file, target):
    featureList1 = list(); featureList2 = list()
    targetIdx = target
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


def getMergedFeature(target, test, flag=0):

    lbl = 1
   
    blast = cur_dir+"/features/test_blast/CLASS_"+str(test)+"_blastFeatures.txt"
    hmm = cur_dir+"/features/test_phmm/CLASS_"+str(test)+"_phmmFeatures.txt"

    featureData_hmm = readFeaturesFromHMMFile(hmm)
    featureData_blast1, featureData_blast2 = readFeaturesFromBlastFile(blast, target)
    # print(len(featureData_blast1), len(featureData_hmm))
    data_sz = min(len(featureData_blast1), len(featureData_hmm))

    # HMM + BLAST 1074*2 features merged
    test_all_feat1 = np.concatenate((featureData_hmm[:data_sz], featureData_blast1[:data_sz]), axis = 1)
    # HMM + BLAST only 3 features merged
    test_all_feat2 = np.concatenate((featureData_hmm[:data_sz], featureData_blast2[:data_sz]), axis = 1)
    # BLAST only 3 features
    test_all_feat3 = featureData_blast2[:data_sz]
    # labels for all
    test_labels = np.full(data_sz, lbl)
    # print(test_all_feat1.shape, featureData_hmm.shape)
    return test_all_feat1, test_all_feat2, test_all_feat3, test_labels


def getScore(target, test_feat, test_labels, modelNo):
    
    modelName = cur_dir+"/models/CLASS_"+str(target)+"_model1_"+ str(modelNo) +".sav"
    clf_blast = pickle.load(open(modelName, 'rb'))

    y_test = clf_blast.predict(test_feat)
    predicted = np.count_nonzero(y_test)
    sc = clf_blast.score(test_feat, test_labels)
    #print(np.nonzero(y_test))
    list1 = list(np.nonzero(y_test)[0])
    return predicted, sc, list1 

###########################################

def predictTP(target, test):
    test_tp_feat1, test_tp_feat2, test_tp_feat3, test_tp_labels = getMergedFeature(target, test, flag=0) # collect v1 feature
    # Model 1 --->  HMM + BLAST 1074*2 features    
    predicted1,sc1,list1 = getScore(target, test_tp_feat1, test_tp_labels, 1)
    # print("########### Model 1 ############")   
    predicted2,sc2,list2 = getScore(target, test_tp_feat2, test_tp_labels, 2)
    # print("########### Model 2 ############")
    predicted3,sc3, list3 = getScore(target, test_tp_feat3, test_tp_labels, 3)
    # print("########### Model 3 ############")

    tp1 =  (set(list1) & set(list2));  
    tp2 = (set(list1) & set(list3))
    tp3 = (set(list2) & set(list3));   
    tp = tp1 | tp2 | tp3 
    
    # print("Ensemble tp count : %d out of\t%d"%(len(tp), len(test_tp_labels)))
    idx = np.zeros(len(test_tp_labels))
    for i in range(len(test_tp_labels)):
        idx[i] = 1 if i in tp else 0
    # print(len(np.where(idx==0)[0]))
    fn = len(test_tp_labels) - len(tp)
    return len(tp),fn,idx


####################################################################    
##################   main function starts here   ###################
####################################################################


famList = np.arange(0,num_class)

test=""

for test in famList:
    fwName = cur_dir+"/result/CLASS_"+str(test)+"_pred.txt"
    
    start = 1
    for target in famList:
        _, _, index = predictTP(target, test)
        if start == 1:
            predictions = np.zeros((num_class, index.shape[0]))
            start = 0
        predictions[target] = index
    
    ###########################  write in file    #########################
    fw=open(fwName,'a')
    for i in range(len(predictions[0])):
        fw.write("%d\t"%i)
        for j in range(num_class):
            if predictions[j][i] == 1:
                fw.write("%d\t"%j)
        fw.write("\n")
    fw.close()

####################################################