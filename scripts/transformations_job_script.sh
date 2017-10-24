#!/bin/bash
#SBATCH --job-name=find_transformations
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=FAIL,END
#SBATCH --output=find_transformations_%a.log
#SBATCH --error=find_transformations_%a.log
source activate mass_spec
# ml load gcc/7.1.0
t=$SLURM_ARRAY_TASK_ID
mkdir ../data/logs/
if [ $t -eq 0 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/BioAge--C8-pos--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 1 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/BioAge--C18-neg--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 2 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/BioAge--HILIC-neg--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 3 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/BioAge--HILIC-pos--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 4 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/MCDS--HILIC-pos--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 5 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/MCDS--LIPID--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 6 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/OE--C8-pos--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 7 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/OE--C18-neg--.txt
	mv find_transformations_${t}.log ../data/logs/ 
elif [ $t -eq 8 ]
	then
	python transformations.py -o ../data/output/ -s ../data/summaries/ ../data/input/OE--HILIC-pos--.txt
	mv find_transformations_${t}.log ../data/logs/ 
fi