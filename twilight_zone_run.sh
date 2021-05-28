#!/bin/bash

cur_dir="$1" # current working directory (e.g. ../GPCR/cv_1)
num_class="$2"

# caculate homology of test set with training set
./homology.sh $cur_dir $num_class
# calculate accuracy
python3 twilight_zone_accuracy.py $cur_dir