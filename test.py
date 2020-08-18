import sys
import numpy as np
from sklearn import svm
from random import randint
import pickle
import random
import math
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

########################3
dataset = sys.argv[1]
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
            st = target*3;      en = st + 3
            data2 = data[st:en]

            featureList1.append(data1);      featureList2.append(data2)

    except FileNotFoundError:
        print(file)

    return np.array(featureList1), np.array(featureList2)

#####  merge blast features and pHMM features together to test ##########

def getMergedFeature(target, file):
    lbl = 1
    
    blast = "../data/features/test_blast/COG_"+str(file)+"_blastFeatures.txt"
    hmm = "../data/features/test_phmm/COG_"+str(file)+"_features.txt"
    
    featureData_hmm = readFeaturesFromHMMFile(hmm)
    featureData_blast1, featureData_blast2 = readFeaturesFromBlastFile(blast, target)
    data_sz = min(len(featureData_blast1), len(featureData_hmm))

    # HMM + BLAST 1074*2 features merged
    test_all_feat1 = np.concatenate((featureData_hmm[:data_sz], featureData_blast1[:data_sz]), axis = 1)
    # HMM + BLAST only 3 features merged
    test_all_feat2 = np.concatenate((featureData_hmm[:data_sz], featureData_blast2[:data_sz]), axis = 1)
    # BLAST only 3 features
    test_all_feat3 = featureData_blast2[:data_sz]
    # labels for all
    test_labels = np.full(data_sz, lbl)

    return test_all_feat1, test_all_feat2, test_all_feat3, test_labels


#########################################################################################################

def getScore(target, test_feat, test_labels, modelNo):

    modelName = "../trained_models/COG_"+str(target)+"_model"+dataset+"_"+ str(modelNo) +".sav"
    clf_blast = pickle.load(open(modelName, 'rb'))

    y_test = clf_blast.predict(test_feat)
    list1 = list(np.nonzero(y_test)[0])
    return list1 

#########################################################################################################
##  return indices of predictions
def getPrediction(target, test_tp_feat1, test_tp_feat2, test_tp_feat3):
    # Model 1 --->  HMM + BLAST 1074*2 features    
    list1 = getScore(target, test_tp_feat1, test_tp_labels, 1)
    # Model 2 --->  HMM + BLAST only 3 features    
    list2 = getScore(target, test_tp_feat2, test_tp_labels, 2)
    # Model 3 --->  BLAST only 3 features    
    list3 = getScore(target, test_tp_feat3, test_tp_labels, 3)

    tp1 = (set(list1) & set(list2))
    tp2 = (set(list2) & set(list3))
    tp3 = (set(list1) & set(list3))
    tp = tp1 | tp2 | tp3

    return tp

###### get predictions for test sequence ############################

def getPredictionAccuracy(output, preds, true_label):
    sz2 = len(preds[0])
    count = 0; correct = 0
    fw = open(output, 'a')
    fw.write("COG_%d\t"%true_label)
    for x in range(sz2):  # calculate accuracy and store indices
        sample = preds[:,x]
        multi_preds = (np.where(sample=="1")[0]) # get the mulitple predictions
        
        if pred_label == "rest":
            if len(multi_preds) > num_pred: # check how many prediction each sample got
                count+=1
                fw.write("%d\t"%x)
                
                if true_label in multi_preds:
                    correct += 1
        else:
            if len(multi_preds) == num_pred: # check how many prediction each sample got
                count+=1
                fw.write("%d\t"%x)
                
                if true_label in multi_preds:
                    correct += 1
        
    fw.write("\n")
    fw.close()
    return correct, count, sz2

##################   get prediction for test sequences   ###################

start = int(sys.argv[3])
end = int(sys.argv[4])

####  get predictions for test sequence ######
fwName = "../data/result/predictions/EnsembleFam_multiple_prediction_"+dataset+".txt"
truePos = 0; totalSample = 0

for true_label in range(start, end):
    fw = open(fwName,'a')
    fw.write(">\tCOG_%d\n"%true_label)
    for target in range(num_class):
        test_tp_feat1, test_tp_feat2, test_tp_feat3, test_tp_labels = getMergedFeature_v3(target, file = true_label )
        pred = getPrediction(target, test_tp_feat1, test_tp_feat2, test_tp_feat3)
        sz = np.arange(0,len(test_tp_labels))
        
        for i in sz:
            if i in pred:
                fw.write("1,")
            else:
                fw.write("0,")
        fw.write("\t")
    fw.write("\n")
    fw.close()
    
#### calculate prediction accuracy in six subgroups ########    
pred_file="../data/result/predictions/EnsembleFam_multiple_prediction_"+dataset+".txt"
with open(pred_file) as f:
    content = f.readlines()
sz = len(content)

num_preds = [1,2,3,4,5,5] # num of prediction in six subgroup
pred_labels = ["single", "two", "three", "four", "five", "rest"]

for num_pred, pred_label in zip(num_preds, pred_labels):

    count = 0; correct = 0; total = 0

    for i in range(0,sz,2):
        true_label = int(content[i].strip().split("_")[1])
        
        data = content[i+1].strip().split("\t")
        preds = list()
        for item in data:  # read predictions for one COG
            p = item.split(",")
            preds.append(np.asarray(p))
        preds = np.asarray(preds)

        temp_corr, temp_cnt, temp_sz = getPredictionAccuracy(file1, preds, true_label)

        correct += temp_corr; count += temp_cnt
        total += temp_sz
        
    print("%s\t%d\t%d\t%d\t%.5f\t%.5f\n"%(pred_label, total, count, correct, correct/count,count/total))
    

