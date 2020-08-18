#!/bin/bash

##################### ##################### #####################
######################### BLAST features #########################
echo "- - - Collecting BLAST features - - - "

dbName="../data/firstTenSeq_100.fasta"

blastPos="../temp_files/cog_blast_pos.txt"
blastDetails="../temp_files/cog_blast_details.txt"
fwName="../data/features/"$1"_blast/"

for sfile in ../data/"$1"_seq/COG_*.fasta; do
# for (( iterator="$1"; iterator<="$2"; iterator++ )); do	
	# sfile="../data/test_seq/COG_$iterator.fasta"
	name=$(echo $sfile | cut -d"/" -f4 | cut -d"." -f1)
	ext="_blast"
	
	blastOut="../data/features/"$1"_blastOut/$name$ext.out"
	blastp -db $dbName -threshold 2 -query $sfile -out $blastOut 

	result=$(grep -n 'Query=' $blastOut | cut -f1 -d: > $blastPos)
	result1=$(grep -n '> ' $blastOut | cut -f1 -d: > $blastDetails)

	python3 extractBlastFeature.py $blastOut $blastPos $blastDetails $fwName $sfile

done

echo "- - - BLAST features Collected! - - - "

##################### ##################### #####################
######################### pHMM features #########################

echo "- - - Collecting pHMM features - - -"

hmmOut="../temp_files/cog_phmm.out"
hmmPos="../temp_files/cog_phmm_pos.txt"
featureFile="../temp_files/cog_phmm_features.txt"

for sfile in ../data/"$1"_seq/COG*.fasta; do

	name=$(echo $sfile | cut -d"/" -f4 | cut -d"." -f1)
	ext="_features"
	fwName="../data/features/phmm_"$1"/$name$ext.txt"

	for filename in ../phmm/*.hmm; do
		##### run hmmscan to gather hmmer score
		../../hmmer/src/./hmmscan --max --acc  -o $hmmOut $filename $sfile
		
		result=$(grep -F -n 'Query:' $hmmOut | cut -f1 -d: > $hmmPos)
		## extract features from hmm output
		python3 extractHMMfeature.py $hmmOut $hmmPos $featureFile 
		
		writeFlag=0
	done

	## convert the feature vectors and store in the feature filename
	python3 column2row.py $featureFile $sfile $fwName

done

echo "- - - BLAST features Collected! - - - "
##################### ##################### #####################
