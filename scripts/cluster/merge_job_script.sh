#!/bin/bash
#SBATCH --job-name=merge
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=16G
#SBATCH --mail-type=FAIL,END
#SBATCH --output=merge_%a.log
#SBATCH --error=merge_%a.log
cd ..
source activate mass_spec
# ml load gcc/7.1.0
t=$SLURM_ARRAY_TASK_ID
mkdir ../data/output/merged/
if [ $t -eq 0 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/BioAge--C8-pos--_adducts.csv \
	-t ../data/output/transformations/BioAge--C8-pos--_transformations.csv \
	-i ../data/output/isoforms/BioAge--C8-pos--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 1 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/BioAge--C18-neg--_adducts.csv \
	-t ../data/output/transformations/BioAge--C18-neg--_transformations.csv \
	-i ../data/output/isoforms/BioAge--C18-neg--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 2 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/BioAge--HILIC-neg--_adducts.csv \
	-t ../data/output/transformations/BioAge--HILIC-neg--_transformations.csv \
	-i ../data/output/isoforms/BioAge--HILIC-neg--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 3 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/BioAge--HILIC-pos--_adducts.csv \
	-t ../data/output/transformations/BioAge--HILIC-pos--_transformations.csv \
	-i ../data/output/isoforms/BioAge--HILIC-pos--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 4 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/MCDS--HILIC-pos--_adducts.csv \
	-t ../data/output/transformations/MCDS--HILIC-pos--_transformations.csv \
	-i ../data/output/isoforms/MCDS--HILIC-pos--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 5 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/MCDS--LIPID--_adducts.csv \
	-t ../data/output/transformations/MCDS--LIPID--_transformations.csv \
	-i ../data/output/isoforms/MCDS--LIPID--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 6 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/OE--C8-pos--_adducts.csv \
	-t ../data/output/transformations/OE--C8-pos--_transformations.csv \
	-i ../data/output/isoforms/OE--C8-pos--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 7 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/OE--C18-neg--_adducts.csv \
	-t ../data/output/transformations/OE--C18-neg--_transformations.csv \
	-i ../data/output/isoforms/OE--C18-neg--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
elif [ $t -eq 8 ]
	then
	python merge.py -o ../data/output/merged/ \
	-a ../data/output/adducts/OE--HILIC-pos--_adducts.csv \
	-t ../data/output/transformations/OE--HILIC-pos--_transformations.csv \
	-i ../data/output/isoforms/OE--HILIC-pos--_isoforms.csv
	
	mv cluster/merge_${t}.log ../data/output/merged/ 
fi