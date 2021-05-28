#!/bin/bash

cur_dir="$1" # current working directory (e.g. ../GPCR/cv_1)
num_class="$2"
train_file="$3" # train file
test_file="$4"  # test file


# preprocess data
python3 preprocessing.py $cur_dir $num_class $train_file $test_file
# create blast db
dbfile="$cur_dir/features/firstTenSeq.fasta"
makeblastdb -in $dbfile -dbtype prot

################## collect blast features
## training feature
./collectBlastFeature.sh $cur_dir train $num_class
## test feature
./collectBlastFeature.sh $cur_dir test $num_class

##################### collect phmm features
## training feature
./collectPhmmFeature.sh $cur_dir train
## test feature
./collectPhmmFeature.sh $cur_dir test

## train svm models
python3 ensemble_models_train.py $cur_dir $num_class
## get predictions for test
python3 ensmeble_models_test.py $cur_dir $num_class


## calculate accuracy
python3 accuracy.py $cur_dir $num_class
