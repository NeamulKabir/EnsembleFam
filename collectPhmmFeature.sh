#!/bin/bash

########################  ###################  #######################
# input 1 - current working directory (../GPCR/cv_1)
# input 2 - train / test
########################  ###################  #######################

echo "- - - Collecting pHMM features - - -"

cur_dir="$1"
hmmOut="../temp_files/temp_hmm$2.out"
hmmPos="../temp_files/temp_hmm_pos$2.txt"
featureFile="../temp_files/temp_hmm_feature_"$2".txt"

outFile="$cur_dir/features/"$2"_phmm/"

for sfile in "$cur_dir"/"$2"_seq/CLASS_*.fasta; do

	echo $sfile
	name=$(echo $sfile | cut -d"/" -f6 | cut -d"." -f1)
	writeFlag=1

	for filename in ../predefined_pHMM/*.hmm; do
			##### run hmmscan to gather hmmer score
			../../../hmmer/src/./hmmscan --max --acc  -o $hmmOut $filename $sfile
			
			result=$(grep -F -n 'Query:' $hmmOut | cut -f1 -d: > $hmmPos)
			## extract features from hmm output
			python3 extractHMMfeature.py $hmmOut $hmmPos $writeFlag $featureFile 
			
			writeFlag=0
		done

		## convert the feature vectors and store in the feature filename  	../temp_files/stock_cog_features_1.txt
		python3 column_2_row.py $featureFile $sfile $outFile

	done