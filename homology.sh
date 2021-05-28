#!/bin/bash
cur_dir="$1"
num_class="$2"

# create directory to store blast data
d1="$1/homology"
mkdir -p $d1
d2="$d1/blastdb"
mkdir -p $d2

###############
for (( iterator=0; iterator<"$num_class"; iterator++ )); do
	sfile="$cur_dir/train_seq/CLASS_"$iterator".fasta"
	# name=$(echo $sfile | cut -d"/" -f6 | cut -d"." -f1)
	dbfile="$cur_dir/homology/blastdb/CLASS_"$iterator".fasta"

	cp $sfile $dbfile

	makeblastdb -in $dbfile -dbtype prot

	testfile="$cur_dir/test_seq/CLASS_"$iterator".fasta"
	ext="_blast"
	blastOut="$cur_dir/homology/blastout/CLASS_"$iterator"$ext.out"

	blastp -db $dbfile -threshold 2 -query $testfile -out $blastOut 

	blastPos="../temp_files/homology_class_pos$1$1$2.txt"
	blastDetails="../temp_files/homology_class_details$1$2.txt"

	result=$(grep -n 'Query=' $blastOut | cut -f1 -d: > $blastPos)
	result1=$(grep -n '> ' $blastOut | cut -f1 -d: > $blastDetails)

	outDir="$cur_dir/homology/test_identities.txt"
	python3 homology_identity.py $blastOut $blastPos $blastDetails $outDir $iterator
done