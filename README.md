# EnsembleFam
EnsembleFam: Towards a more accurate protein function prediction in twilight zone

EnsembleFam aims at better function prediction for proteins in the twilight zone. EnsembleFam extracts the core characteristics of a protein family
using similarity and dissimilarity features calculated from sequence homology relations. EnsembleFam trains three separate Support Vector Machine (SVM) 
classifiers for each family using these features, and an ensemble prediction is made to classify novel proteins into these families. 

# Instructions to execute

## Requirements
To execute EnsembleFam the following requirements need to be fullfilled:
 * Python 3
 * HMMER v3.2.1
 * BLASTP
 * Scikit-learn

## Data file
Data file used in training and testing EnsembleFam can be downloaded from here. In the data file, EnsmebleFam requires all the sequences and their respective labels separated by tab character in one file, i.e. all training sequences in one file.

## Command to execute
The bash script `run.sh` executes all the steps of EnsembleFam one by one and returns overall accuracy on the test set. This command requires four parameters in the following order: 
1. *cur_dir* : current working directory where all the feature files and trained models will be stored (e.g. `../data`)
2. *num_class* : number of class (e.g. 86 for GPCR sub-subfamilies)
3. *train_file* : training file (e.g. `../data/train.txt`)
4. *test_file* : test file (e.g. `../data/test.txt`)

An example command to execute EnsembleFam: `./run.sh  ../data  86  ../data/train.txt  ../data/test.txt`

**Note:** Feature collection using BLAST may require some time depending on the data size.

## Twilight zone accuracy
To calculate twilight zone accuracy or homology based accuracy, bash script `twilight_zone_run.sh` command can be used. It first calcuates the homology between training and test set, then calculates  accuracy for different identity level. To run this command, `run.sh` needs to be executed first. `twilight_zone_run.sh` requires two parameters: *cur_dir* and *num_class*.

Example: `./twilight_zone_run.sh ../data 86`


