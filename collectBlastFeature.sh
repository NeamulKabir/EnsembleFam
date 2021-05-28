#!/bin/bash

##################### ##################### #####################
#input 1 - current working directory (../GPCR/cv_1)
#input 2 - train / test
#input 3, 4 - start and end num of family
######################### BLAST features #########################
echo "- - - Collecting $2 BLAST features - - - "

cur_dir=$1
num_class=$3
dbName=""$cur_dir"/features/firstTenSeq.fasta"


blastPos="../temp_files/"$2"_blast_pos$1$3.txt"
blastDetails="../temp_files/"$2"_blast_details$1$3$4.txt"

fwName=""$cur_dir"/features/"$2"_blast/"


for (( iterator=0; iterator<"$num_class"; iterator++ )); do	

	sfile=""$cur_dir"/"$2"_seq/CLASS_"$iterator".fasta"

	name=$(echo $sfile | cut -d"/" -f6 | cut -d"." -f1)
	ext="_blast"
	blastOut=""$cur_dir"/features/"$2"_blastOut/$name$ext.out"
	blastp -db $dbName -threshold 2 -query $sfile -out $blastOut 

	result=$(grep -n 'Query=' $blastOut | cut -f1 -d: > $blastPos)
	result1=$(grep -n '> ' $blastOut | cut -f1 -d: > $blastDetails)

	python3 extractBlastFeature.py $blastOut $blastPos $blastDetails $fwName $num_class

done
