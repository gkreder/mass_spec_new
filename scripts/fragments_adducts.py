################################################################################
# Gabe Reder - gkreder@gmail.com
# 08/2017
################################################################################
import sys
import os
import time
import math
from xlrd import open_workbook
import itertools
from aux import *
start_time = time.time()
################################################################################
# Parameters
################################################################################
delimiter = ','
rt_tolerance = 0.03
mz_tolerance = 0.005
################################################################################
# Read Input Arguments
################################################################################
test = False
move_output = False
move_summary = False
if len(sys.argv) < 2:
	sys.exit('''\t Error: must specify input file
				USAGE: python fragments_adducts.py [args] input_file
				args:
					-t: tolerance in RT units (default 0.03)
					-d: delimiter for output files (default ',' )
					-o: output directory
					-s: summary directory
					-m: mz tolerance (default 0.005) ''')
for i, arg in enumerate(sys.argv[1 : -1]):
	if arg[0] == '-':
		if sys.argv[i + 2][0] == '-' or i == len(sys.argv[1 : -1]) - 1:
			if arg[0 : 2] != '--':
				sys.exit('Error: Hanging argument flag')
	if arg == '-t':
		tolerance = float(sys.argv[i + 2])
	if arg == '-d':
		delimiter = sys.argv[i + 2]
	if arg == '--test':
		test = True
	if arg == '-m':
		mz_tolerance = float(sys.argv[i + 2])
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

if sys.argv[-2][0] == '-' and sys.argv[-2][0 : 2] != '--':
	sys.exit('''Error: must specify input file''')
in_file = sys.argv[-1]
################################################################################
# Main Script
################################################################################
# Transformations dictionary for searching reactions
# open transformations worksheet
wb = open_workbook('../data/transformations.xlsx')
transformation_sheet = wb.sheet_by_name('Common adducts')
# Save mz vals and adduct names (removing blank rows)
mz_list = [x.value for x in transformation_sheet.col(1)[1 : ] if x.value != '']
names = [x.value for x in transformation_sheet.col(0)[1 : ] if x.value != '']
# modes = [x.value for x in transformation_sheet.col(2)[1 : ] if x.value != '']
mz_list_pos = [x.value for i,x in enumerate(transformation_sheet.col(1)[1 : ]) \
	if x.value != '' \
	and transformation_sheet.col(2)[1 : ][i].value != 'negative']
names_pos = [x.value for i,x in enumerate(transformation_sheet.col(0)[1 : ]) \
	if x.value != '' \
	and transformation_sheet.col(2)[1 : ][i].value != 'negative']
mz_list_neg = [x.value for i,x in enumerate(transformation_sheet.col(1)[1 : ]) \
	if x.value != '' \
	and transformation_sheet.col(2)[1 : ][i].value != 'positive']
names_neg = [x.value for i,x in enumerate(transformation_sheet.col(0)[1 : ]) \
	if x.value != '' \
	and transformation_sheet.col(2)[1 : ][i].value != 'positive']

if len(mz_list) != len(names):
	sys.exit('Error: Column length mismatch in transformation excel input...'\
	+ 'does every adduct have both a name and mz value?')

if len(mz_list_neg) != len(names_neg):
	sys.exit('Error: Column length mismatch in transformation excel input...'\
	+ 'does every adduct have both a name and mz value?')

if len(mz_list_pos) != len(names_pos):
	sys.exit('Error: Column length mismatch in transformation excel input...'\
	+ 'does every adduct have both a name and mz value?')
# Save transformations (adducts) - NOTE dict keys are mz values and the values
# are the reaction names
# transformations = dict(zip(mz_list, names))
transformations_pos = dict(zip(mz_list_pos, names_pos))
transformations_neg = dict(zip(mz_list_neg, names_neg))

# Want transformations (and corresponding delta_mz values) BETWEEN the
# adducts in the sheet, not the actual mz values themselves 
def temp_string(x,y, d):
	return d[y] + '--->' + d[x]
temp_pos = [(x-y, temp_string(x,y,transformations_pos)) \
	for (x,y) in itertools.combinations(transformations_pos, 2) \
	if 'M+1' not in transformations_pos[x] and 'M+1' not in transformations_pos[y]]
temp_pos_2 = [(y-x, temp_string(y,x,transformations_pos)) \
	for (x,y) in itertools.combinations(transformations_pos, 2) \
	if 'M+1' not in transformations_pos[x] and 'M+1' not in transformations_pos[y]]
temp_pos_3 = [(x, transformations_pos[x]) for x in transformations_pos \
			if 'M+1' in transformations_pos[x]]
temp_pos = temp_pos + temp_pos_2 + temp_pos_3
transformations_pos = dict(zip([x for (x,y) in temp_pos], \
	[y for (x,y) in temp_pos]))

temp_neg = [(x-y, temp_string(x,y,transformations_neg)) \
	for (x,y) in itertools.combinations(transformations_neg, 2) \
	if 'M+1' not in transformations_neg[x] and 'M+1' not in transformations_neg[y]]
temp_neg_2 = [(y-x, temp_string(y,x,transformations_neg)) \
	for (x,y) in itertools.combinations(transformations_neg, 2) \
	if 'M+1' not in transformations_neg[x] and 'M+1' not in transformations_neg[y]]
temp_neg_3 = [(x, transformations_neg[x]) for x in transformations_neg \
			if 'M+1' in transformations_neg[x]]
temp_neg = temp_neg + temp_neg_2 + temp_neg_3
transformations_neg = dict(zip([x for (x,y) in temp_neg], \
	[y for (x,y) in temp_neg]))

mz_list_pos = [x for x in transformations_pos]
mz_list_neg = [x for x in transformations_neg]
max_diff_pos = max([abs(x) for x in transformations_pos.keys()])
max_diff_neg = max([abs(x) for x in transformations_neg.keys()])


# max_diff = max([abs(x) for x in transformations.keys()])

# Open data file and readlines (ignoring NA lines)
with open(in_file, 'r') as f:
	lines = [line.strip() for line in f if 
				get_mz_in(line).upper() != 'NA' \
				and get_rt_in(line).upper() != 'NA']
# Throw away header line
lines = lines[1 : ]
# Sort lines by rt value (smallest to largest)
lines = sorted(lines, key = lambda line : float(line.split('\t')[3]))
# Testing subsets of the data for timing
if test:
	lines = lines[0 : 500]
saved_lines = {}
# For sliding window to not check metabolites that you shouldn't have to
j_start = 0
# For counting number of metabolites per method
method_counts = {}
for i, line_outer in enumerate(lines):
	check_time(i, lines, start_time)
	method = get_method_in(line_outer)
	if method in method_counts:
		method_counts[method] = method_counts[method] + 1
	else:
		method_counts[method] = 1
	# for j, line_inner in enumerate(lines):
	j_temp = j_start
	for j in range(j_start, len(lines)):
		line_inner = lines[j]
		delta_rt = float(get_rt_in(line_inner)) - float(get_rt_in(line_outer))
		if abs(delta_rt) > rt_tolerance:
			if j >= i:
				break
			else:
				if j > j_start:
					j_temp = j
				continue
		if method == get_method_in(line_inner):
			delta_mz = float(get_mz_in(line_inner)) - float(get_mz_in(line_outer))
			if 'pos' in method:
				check_list = mz_list_pos
				check_transformations = transformations_pos
			else:
				check_list = mz_list_neg
				check_transformations = transformations_neg
			closest_match = min(check_list, key = \
										 lambda x : min(
										 	abs(x - delta_mz),
										 	abs(x + delta_mz))
										 )
			dist_current = abs(closest_match - delta_mz)
			# I don't think I want the reverse check for adducts?
			# dist_reverse = abs(closest_match + delta_mz)

			# if min(dist_current, dist_reverse) <= mz_tolerance:
			if dist_current <= mz_tolerance: 
				line_to = line_inner
				line_from = line_outer
				# if dist_reverse < dist_current:
				# 	line_to = line_outer
				# 	line_from = line_inner
				if method in saved_lines:
					saved_lines[method].append(join_trans_lines(closest_match, 
										 				 line_from,
										 				 line_to,
										 				 check_transformations,
										 				 delimiter))
				else:
					saved_lines[method] = [join_trans_lines(closest_match,
													 line_from,
													 line_to,
													 check_transformations,
													 delimiter)]
	j_start = j_temp
num_found_transformations = 0
for method in saved_lines:
	num_found_transformations += len(saved_lines[method])
	# out_file = in_file.split('_')[0].split('.')[0] + '_' + method+'_adducts.csv'
	out_file = in_file.replace('.txt', '_adducts.csv')
	with open(out_file, 'w') as f:
		print(get_header(delimiter), file = f)
		for line in saved_lines[method]:
			print(line, file = f)
	if move_output:
		os.system('mv ' + out_file + ' ' + out_dir)
if len(saved_lines) == 0:
	print('Warning: Empty saved_lines variable - assuming only one method: ' +\
			in_file.split('_')[0].split('.')[0])
	first_string = in_file.split('_')[0].split('.')[0]
	out_file = first_string + '_' + \
		first_string[first_string.index('(') + 1 : first_string.index(')')] \
		+ '_adducts.csv'
	with open(out_file, 'w') as f:
		print(get_header(delimiter), file = f)
# summary_file = in_file.split('_')[0].split('.')[0] + '_' + \
	# str(rt_tolerance).replace('.', '-') + '_adduct_summary.txt'
summary_file = in_file.replace('.txt', '_adducts_summary.txt')
with open(summary_file, 'w') as f:
	print('-----------------------------------------------------------', file=f)
	print('Input file --- ' + in_file, file = f)
	print('System Call --- ' + ' '.join(sys.argv), file = f)
	print('Tolerance (rt) --- ' + str(rt_tolerance), file = f)
	print('-----------------------------------------------------------', file=f)
	print('*Total*', file = f)
	print('Total Metabolites (no NA) --- ' + str(len(lines)), file = f)
	print('Total found adducts --- ' + \
		str(num_found_transformations), file=f)
	print('', file = f)
	for method in saved_lines:
		print('*' + method + '*', file = f)
		print('Number metabolites (' + method + ') --- ' + \
			str(method_counts[method]), file = f)
		print('Found adducts (' + method + ') --- ' + \
			str(len(saved_lines[method])), file = f)
		print('', file = f)
if move_summary:
	os.system('mv ' + summary_file + ' ' + summary_dir)
elif move_output:
	os.system('mv ' + summary_file + ' ' + out_dir)
end_time = time.time()
print('Total time elapsed - ' + str(end_time - start_time))