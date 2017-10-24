################################################################################
# Gabe Reder - gkreder@gmail.com
# 08/2017
################################################################################
import sys
import os
import time
from aux import *
start_time = time.time()
################################################################################
# Read Input Arguments and setup folder tree
################################################################################
adduct_tolerance = 0.1
top_dir = os.getcwd() + '/'
test = False
found_adduct_file = False
found_transformation_file = False
move_output = False
move_summary = False
file_name = ''
if len(sys.argv) < 2:
	# sys.exit('''\t Error: must specify input directory

	# 			USAGE: python [-d adduct_tolerance -n file_name] ''' + \
	# 			'fast_merge.py directory_name')
	sys.exit('''\t Error: must specify adduct and transformation files

			USAGE: python [-d adduct_tolerance] -a adduct_file 
			-a: adduct file
			-t: transformation file
			-o: output directory
			-s: summary directory
			''' + \
			' -t transformation_file fast_merge.py')

for i, arg in enumerate(sys.argv[1 : -1]):
	# if arg[0] == '-':
		# if sys.argv[i + 2][0] == '-' or i == len(sys.argv[1 : -1]) - 1:
		# 	if arg[0 : 2] != '--':
		# 		sys.exit('Error: Hanging argument flag')
	if arg == '-d':
		adduct_tolerance = float(sys.argv[i + 2])
	if arg == '--test':
		test = True
	if arg =='-a':
		found_adduct_file = True
		adduct_fname = sys.argv[i + 2]
	if arg =='-t':
		found_transformation_file = True
		transformation_fname = sys.argv[i + 2]
	if arg == '-o':
		out_dir = sys.argv[i + 2]
		out_dir = os.path.abspath(out_dir)
		if out_dir[-1] != '/':
			out_dir = out_dir + '/'
		move_output = True
	if arg == '-s':
		summary_dir = sys.argv[i + 2]
		summary_dir = os.path.abspath(summary_dir)
		if summary_dir[-1] != '/':
			summary_dir = summary_dir + '/'
		move_summary = True

if not found_adduct_file or not found_transformation_file:
	sys.exit('''\t Error: must specify adduct and transformation files

		USAGE: python [-d adduct_tolerance] -a adduct_file ''' + \
		' -t transformation_file fast_merge.py')

# if sys.argv[-1][0] == '-':
	# sys.exit('''Error: Hanging argument flag''')

in_folder = top_dir + sys.argv[-1]
out_folder = in_folder + '/../output/'
# if 'output' not in os.listdir(in_folder + '/../'):
	# os.system('mkdir ' + out_folder)
################################################################################
# Initialize file lists and header
################################################################################
# os.chdir(in_folder)
# trans_files = [x for x in os.listdir() if x[0] != '.' \
# 	and '_transformations.csv' in x \
# 	and 'merged' not in x]
# adduct_files = [x for x in os.listdir() if x[0] != '.' \
# 	and '_adducts.csv' in x \
# 	and 'merged' not in x]

# Left-over from old way of scraping input files, need to rewrite at some point
trans_files = [transformation_fname]
adduct_files = [adduct_fname]
cohorts = {}

# check to make sure every transformation file has a coresponding
# adduct file
adduct_check = [x.split('_adducts.csv')[0] for x in adduct_files]
for i, x in enumerate(trans_files):
	name = x.split('_transformations.csv')[0]
	if name not in adduct_check:
		sys.exit('Error: Couldn\'t find corresponding adduct file for ' +\
			'transformation file ' + name)
if len(adduct_files) != len(trans_files):
	sys.exit('Error: Each transformation file must have an adduct file and \
		vice versa')
# Save cohort names and header line
for f in trans_files:
	if f.split('_')[0] not in cohorts:
		cohorts[f.split('_')[0]] = []
with open(f, 'r') as f:
	header = f.readline().strip()
################################################################################
# Helper functions for reading/storing redundant adducts
################################################################################
# Get redundant adducts according to adducts dict
def get_redun_adducts(metab, adducts):
	redun = []
	if metab in adducts:
		redun = adducts[metab]
	return redun

# Given trans_from metabolite and trans_to metabolite, and dictionary of found
# transformations, and adducts dictionary - checks if the proposed reaction
# trans_from ---> trans_to is redundant (according to adducts dict)
def is_redun(trans_from, trans_to, adducts, found_trans):
	found = False
	redun_from_list = get_redun_adducts(trans_from, adducts)
	redun_to_list = get_redun_adducts(trans_to, adducts)
	redun_from_list.append(trans_from)
	redun_to_list.append(trans_to)
	for x_from in redun_from_list:
		if x_from in found_trans:
			for x_to in redun_to_list:
				if x_to in found_trans[x_from]:
					found = True
	return found
# Record the new transformation trans_from--->trans_to and all redundant ones 
# too according to adducts
def update_transformations(trans_from, trans_to, adducts, found_trans):
	redun_from_list = get_redun_adducts(trans_from, adducts)
	redun_to_list = get_redun_adducts(trans_to, adducts)
	redun_from_list.append(trans_from)
	redun_to_list.append(trans_to)
	for x_from in redun_from_list:
		for x_to in redun_to_list:
			if x_from in found_trans:
				found_trans[x_from].append(x_to)
			else:
				found_trans[x_from] = [x_to]
	return found_trans
################################################################################
# Main filtering and storing script
################################################################################
# Filter each transformation file using corresponding adduct file and keep
# non-redundant transformations
cohort_summaries = {}
for cohort_i, cohort in enumerate(cohorts):
	cohort_summaries[cohort] = []
	file_summaries = []
	print(cohort + ' (' + str(cohort_i + 1) + ' of ' + str(len(cohorts)) +')')
	cohorts[cohort].append(header)
	# sort to make sure the indices are common between the two
	cohort_trans = sorted([x for x in trans_files if cohort in x])
	cohort_adducts = sorted([x for x in adduct_files if cohort in x])
	for file_index, file in enumerate(cohort_trans):
		summary_name = file.split('_transformations.csv')[0]
		num_adducts = 0
		print('\t***' + summary_name + '***')
		num_redun = 0
		num_recorded = 0
		adducts = {}
		found_trans = {}
		# Save adducts for given cohort-method adduct file
		with open(cohort_adducts[file_index], 'r') as f:
			print('\tSaving Adducts...')
			loop_lines = f.readlines()[1 : ]
			if test:
				loop_lines = loop_lines[ : 100]
			for x in loop_lines:
				# Only keep adduct lines within tolerance
				if get_adduct_err(x) <= adduct_tolerance:
					num_adducts += 1
					if get_adduct_from(x) in adducts:
						adducts[get_adduct_from(x)].append(get_adduct_to(x))
					else:
						adducts[get_adduct_from(x)] = [get_adduct_to(x)]
		print('\t...done')
		trans_lines = []
		# Save list of non-redundant found transformations in cohort-method
		# transformation file
		with open(file, 'r') as f:
			print('\tFiltering candidate transformations...')
			loop_lines = f.readlines()[1 : ]
			if test:
				loop_lines = loop_lines[ : 100]
			for trans_index, x in enumerate(loop_lines):
				check_time(trans_index, loop_lines, start_time, tabs = 1)
				trans_from = get_trans_from(x)
				trans_to = get_trans_to(x)
				# check if redundant transformation
				if is_redun(trans_from, trans_to, adducts, found_trans):
					num_redun += 1
					continue
				# If gets to here, then non-redundant
				trans_lines.append(x.strip())
				num_recorded += 1
				# Add transformation and redunant transformations to found_trans
				found_trans = update_transformations(trans_from, trans_to, \
					adducts, found_trans)
		for line in trans_lines:
			cohorts[cohort].append(line)
		# save file summary
		summary_files = file + ', ' + cohort_adducts[file_index]
		cohort_summaries[cohort].append((summary_name, summary_files, \
			num_recorded, num_redun, num_adducts))
	# write outfile (merged.csv file) for each cohort
	# out_file = cohort + '_merged.csv'
	out_file = adduct_fname.replace('_adducts.csv', '_merged.csv')
	with open(out_file, 'w') as f:
		for line in cohorts[cohort]:
			print(line, file = f)
	if move_output:
		os.system('mv ' + out_file + ' ' + out_dir)
	print('...done --- ' + str(time.time() - start_time) + ' seconds elapsed')
################################################################################
# Print summary files
################################################################################
print('Writing summary files')
for cohort in cohorts:
	# summary_file = cohort + '_' + '_merged_summary.txt'
	summary_file = adduct_fname.replace('_adducts.csv', '_merged_summary.txt')
	total_recorded = 0
	total_redun = 0
	total_adducts = 0
	with open(summary_file, 'w') as f:
		print('-------------------------------------------------------', file=f)
		print('Input directory --- ' + in_folder, file = f)
		print('System call --- ' + ' '.join(sys.argv), file = f)
		print('Adduct tolerance --- ' + str(adduct_tolerance), file = f)
		print('Total runtime --- ' + \
			str(round((time.time() - start_time) / 60, 2)) + \
			' minutes', file = f)
		print('-------------------------------------------------------', file=f)
		for (summary_name, summary_files, num_recorded, num_redun, num_adducts)\
			in cohort_summaries[cohort]:
			print('', file = f)
			print('*' + summary_name +'*', file = f)
			print('Files --- ' + summary_files, file = f)
			print('Transformations kept --- ' + str(num_recorded), file = f)
			print('Transformations discarded --- ' + str(num_redun), file = f)
			print('Original Transformations --- ' + \
				str(num_redun + num_recorded), file = f)
			print('Number of adducts tested --- ' + str(num_adducts), file = f)
			print('', file= f)
			total_recorded += num_recorded
			total_redun += num_redun
			total_adducts += num_adducts
		print('*Total*', file = f)
		print('Transformation kept --- ' + str(total_recorded), file = f)
		print('Transformation discarded --- ' + str(total_redun), file = f)
		print('Original Transformations --- ' + \
				str(total_redun + total_recorded), file = f)
		print('Number of adducts tested --- ' + str(total_adducts), file = f)
	if move_summary:
		os.system('mv ' + summary_file + ' ' + summary_dir)
	elif move_output:
		os.system('mv ' + summary_file + ' ' + out_dir)
print('...done --- ' + str(time.time() - start_time) + ' seconds elapsed')