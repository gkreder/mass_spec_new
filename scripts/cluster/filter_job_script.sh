#!/bin/bash
#SBATCH --job-name=filter
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=FAIL,END
#SBATCH --output=filter_%a.log
#SBATCH --error=filter_%a.log
cd ..
source activate mass_spec
# ml load gcc/7.1.0
t=$SLURM_ARRAY_TASK_ID
mkdir ../data/output/merged/
if [ $t -eq 0 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/BioAge--C8-pos--_knowns.txt \
	../data/output/BioAge--C8-pos--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 1 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/BioAge--C18-neg--_knowns.txt \
	../data/output/BioAge--C18-neg--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 2 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/BioAge--HILIC-neg--_knowns.txt \
	../data/output/BioAge--HILIC-neg--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 3 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/BioAge--HILIC-pos--_knowns.txt \
	../data/output/BioAge--HILIC-pos--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 4 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/MCDS--HILIC-pos--_knowns.txt \
	../data/output/MCDS--HILIC-pos--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 5 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/MCDS--LIPID--_knowns.txt \
	../data/output/MCDS--LIPID--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 6 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/OE--C8-pos--_knowns.txt \
	../data/output/OE--C8-pos--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 7 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/OE--C18-neg--_knowns.txt \
	../data/output/OE--C18-neg--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
elif [ $t -eq 8 ]
	then
	python filter.py -o ../data/output/filtered/ \
	-k ../data/knowns/OE--HILIC-pos--_knowns.txt \
	../data/output/OE--HILIC-pos--_merged.csv
	
	mv cluster/filter_${t}.log ../data/output/filtered/ 
fi