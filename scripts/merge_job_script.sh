#!/bin/bash
#SBATCH --job-name=merge
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=FAIL,END
#SBATCH --output=merge_%a.log
#SBATCH --error=merge_%a.log
source activate mass_spec
# ml load gcc/7.1.0
t=$SLURM_ARRAY_TASK_ID
mkdir ../data/logs/
if [ $t -eq 0 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/BioAge--C8-pos--_adducts.csv -t ../data/output/BioAge--C8-pos--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 1 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/BioAge--C18-neg--_adducts.csv -t ../data/output/BioAge--C18-neg--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 2 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/BioAge--HILIC-neg--_adducts.csv -t ../data/output/BioAge--HILIC-neg--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 3 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/BioAge--HILIC-pos--_adducts.csv -t ../data/output/BioAge--HILIC-pos--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 4 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/MCDS--HILIC-pos--_adducts.csv -t ../data/output/MCDS--HILIC-pos--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 5 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/MCDS--LIPID--_adducts.csv -t ../data/output/MCDS--LIPID--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 6 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/OE--C8-pos--_adducts.csv -t ../data/output/OE--C8-pos--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 7 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/OE--C18-neg--_adducts.csv -t ../data/output/OE--C18-neg--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
elif [ $t -eq 8 ]
	then
	python merge.py -o ../data/output/ -s ../data/summaries/ -a ../data/output/OE--HILIC-pos--_adducts.csv -t ../data/output/OE--HILIC-pos--_transformations.csv
	mv merge_${t}.log ../data/logs/ 
fi