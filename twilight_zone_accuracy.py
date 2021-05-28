import sys
from collections import Counter
from sklearn.model_selection import train_test_split
from brokenaxes import brokenaxes
import numpy as np
import glob
import matplotlib.pyplot as plt
from sklearn import metrics

cur_dir = sys.argv[1]

file = cur_dir + "/homology/test_identities.txt"
with open(file) as f:
    content = f.readlines()

identities = [0,30,40,50,60,100] ## different identity level
for i in range(5):
    start = identities[i]; end = identities[i+1]
    tpval = 0; fnval = 0
    for line in content:
        data = line.strip().split("\t")
        idxlist = list()
        for it, item in enumerate(data[1:]):
            if int(item)>start and int(item)<=end:
                idxlist.append(it)
            elif start==0 and int(item)==start:
                idxlist.append(it)

        if len(idxlist)>0:
            target = data[0]
            filename=cur_dir + "/result/CLASS_"+target+"_pred.txt"
            with open(filename) as f:
                content2 = f.readlines()

            for val in idxlist:
                data = content2[val].strip().split("\t")
                if target in data[1:]:
                    tpval += 1
                else:
                    fnval += 1

    accu = tpval / (tpval + fnval)                
    print("Accuracy for identity level %d to %d: %.4f\n"%(start, end, accu))