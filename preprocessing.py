import sys
from collections import Counter
from sklearn.model_selection import train_test_split
from brokenaxes import brokenaxes
import numpy as np
import glob
import matplotlib.pyplot as plt
import os

########  input arguments    ############
cur_dir = sys.argv[1] ## current working directory e.g. ../GPCR/cv_1
num_class = int(sys.argv[2])
train_file = sys.argv[3]
test_file = sys.argv[4]
##### step 1 #############
def createDirectories():
	train = cur_dir +"/train_seq"
	test = cur_dir +"/test_seq"
	feat = cur_dir +"/features"
	blast_tr = cur_dir +"/features/train_blast"
	blast_ts = cur_dir +"/features/test_blast"
	blastout_tr = cur_dir +"/features/train_blastOut"
	blastout_ts = cur_dir +"/features/test_blastOut"
	hmm_tr = cur_dir +"/features/train_phmm"
	hmm_ts = cur_dir +"/features/test_phmm"
	temp = "../temp_files"
	model = cur_dir +"/models"
	result = cur_dir + "/result"
	try:
	    os.mkdir(train)
	    os.mkdir(test)
	    os.mkdir(feat)
	    os.mkdir(blast_tr)
	    os.mkdir(blast_ts)
	    os.mkdir(hmm_tr)
	    os.mkdir(hmm_ts)
	    os.mkdir(temp)
	    os.mkdir(model)
	    os.mkdir(result)
	    os.mkdir(blastout_tr)
	    os.mkdir(blastout_ts)
	except OSError:
	    print("failed to create directory")
	return
########################################
def readTrainTest(filename, train_test=0):
	#####. step 2
	if train_test == 1:
		cur_val = "train"
	else:
		cur_val = "test"

	for cur_val in train_test:
	    filename = cur_dir + "/" + cur_val + ".txt"
	    with open(filename) as f:
	        content =f.readlines()
	    print(len(content))
	    
	    count = np.zeros(num_class,)
	    for line in content:
	        data = line.strip().split("\t")
	        class_id = data[0]
	        seq = data[1].replace('_','')
	        file = cur_dir  + "/" + cur_val + "_seq/CLASS_" + class_id + ".fasta"
	        fa = open(file, 'a')
	        fa.write(">\t%s_%d\n%s\n" % (class_id, count[int(class_id)], seq) )
	        fa.close()
	        count[int(class_id)] += 1
	return

##################################################
def createBlastDB():
	#####  Step 3
	blastdb = cur_dir  + "/features/firstTenSeq.fasta"
	minSeq = 10

	for i in range(num_class):
	    file = cur_dir  + "/train_seq/CLASS_" + str(i) + ".fasta"
	    with open(file) as f:
	        content = f.readlines()
	    tempCount = 0
	    sz = len(content)
	    for it in range(0,sz,2):
	        fw = open(blastdb,'a')
	        fw.write(content[it])
	        fw.write(content[it+1])
	        tempCount += 1
	        if tempCount == minSeq:
	            break
	return

############################################


### main function ###
# create some directories 
createDirectories()

# read train file
readTrainTest(train_file, train_test=1)

# read test file
readTrainTest(test_file, train_test=0)

# create blast db for feature collection
createBlastDB()
