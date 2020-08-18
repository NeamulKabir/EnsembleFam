import sys
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import math
import time


num_features = 1074

blastFile = sys.argv[1]
posFile = sys.argv[2]
posDetails = sys.argv[3]
name = sys.argv[5].split("/")[-1].split(".")[0]   #### cog 500
fwName = sys.argv[4]+ name  + "Features.txt" ### "../cog_data/data/features/COG_"
print(fwName)

with open(blastFile) as f:
    content_blast = f.readlines()

with open(posFile) as f:
    content_pos = f.readlines()

with open(posDetails) as f:
    content_details = f.readlines()

fw = open(fwName,'w')
iterator = 0; detail_len = len(content_details); pos_len = len(content_pos); blast_len = len(content_blast)

start_time = time.time()

iterator = 0;  line_cnt = 0
for i in range(pos_len):
    if i == len(content_pos)-1:
        next_pos = blast_len - 1
    else:
        next_pos = int(content_pos[i+1].strip())
    
    score_vals = np.full(num_features, 0.0)
    eval_vals = np.full(num_features, 0.0)
    ident_vals = np.full(num_features, 0.0)
    
    val = int(content_details[iterator].strip())
    while(val < next_pos):
        cog_val = int(content_blast[val-1].strip().split()[1].split("_")[0])
        cog_length = int(content_blast[val].strip().split('=')[1])
        if score_vals[cog_val] == 0.0:
            
            line1 = content_blast[val+2].strip().split()
            line2 = content_blast[val+3].strip().split()
            ident = int(line2[2].strip().split("/")[0])

            ident_vals[cog_val] = ident; 
            score_vals[cog_val] = float(line1[2]);   
            temp_e = (line1[7].split(',')[0])
            eval_vals[cog_val] = -999 if temp_e == "0.0" else math.log(float(temp_e)) 
            
        iterator += 1
        if iterator == detail_len:
            break
        val = int(content_details[iterator].strip())

    for j in range(num_features):
    	fw.write("%.5f\t%.5f\t%d\t" % (score_vals[j],eval_vals[j], ident_vals[j]))
    fw.write("\n")
    
    line_cnt += 1
fw.close()
# print("--- %s seconds ---" % (time.time() - start_time))