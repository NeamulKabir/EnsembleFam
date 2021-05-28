import sys
from collections import Counter
from sklearn.model_selection import train_test_split
from brokenaxes import brokenaxes
import numpy as np
import glob
import matplotlib.pyplot as plt
from sklearn import metrics

##########################################
cur_dir = sys.argv[1]
num_class = int(sys.argv[2])
##########################################

tp_val = np.zeros(num_class,)
fp_val = np.zeros(num_class,)
true_count = np.zeros(num_class,)

for target in range(num_class):
    filename = cur_dir +"/result/CLASS_" + str(target) +"_pred.txt"

    with open(filename) as f:
        content = f.readlines()

    true_count[target] = len(content)
    for line in content:
        data = line.strip().split("\t")
        for item in data[1:]:
            val = int(item)
            if val == target:
                tp_val[val] += 1
            else:
                fp_val[val] += 1
total_test = np.sum(true_count)
accu = np.full(num_class,0.0)
for i in range(num_class):
    fn = true_count[i] - tp_val[i]
    tn = total_test - (tp_val[i] + fp_val[i] + fn)
    accu[i] = (tp_val[i] + tn) / total_test

accuracy =  (np.average(accu))

print(accuracy)