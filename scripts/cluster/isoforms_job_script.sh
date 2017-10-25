#!/bin/bash
#SBATCH --job-name=isoforms
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=FAIL,END
#SBATCH --output=isoforms_%a.log
#SBATCH --error=isoforms_%a.log
cd ..
source activate mass_spec
# ml load gcc/7.1.0
t=$SLURM_ARRAY_TASK_ID
mkdir ../data/output/isoforms/
if [ $t -eq 0 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/BioAge--C8-pos--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 1 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/BioAge--C18-neg--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 2 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/BioAge--HILIC-neg--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 3 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/BioAge--HILIC-pos--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 4 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/MCDS--HILIC-pos--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 5 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/MCDS--LIPID--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 6 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/OE--C8-pos--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 7 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/OE--C18-neg--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
elif [ $t -eq 8 ]
	then
	python isoforms.py -o ../data/output/isoforms/ ../data/input/OE--HILIC-pos--.txt
	mv cluster/isoforms_${t}.log ../data/output/isoforms/ 
fi