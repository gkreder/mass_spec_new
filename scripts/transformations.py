################################################################################
# Gabe Reder - gkreder@gmail.com
# 08/2017
# 
# Finds candidate relationships between metabolites 
################################################################################
import sys
import os
import time
from xlrd import open_workbook
from aux import *
start_time = time.time()
################################################################################
# parameters
################################################################################
delimiter = ','
tolerance = 0.01
################################################################################
# Read Input Arguments
################################################################################
test = False
move_output = False
move_summary = False
if len(sys.argv) < 2:
	sys.exit('''\t Error: must specify input file
				USAGE: python transformations.py [args] input_file
				args:
					-t: tolerance (in m/z units, default 0.01)
					-d: delimiter for output files (default ',' )
					-o: output directory
					-s: summary directory''')
for i, arg in enumerate(sys.argv[1 : -1]):
	if arg[0] == '-':
		if sys.argv[i + 2][0] == '-' or i == len(sys.argv[1 : -1]) - 1:
			if arg[0 : 2] != '--':
				sys.exit('Error: Hanging argument flag')
	if arg == '-t':
		tolerance = float(sys.argv[i + 2])
	if arg == '-d':
		delimiter = sys.argv[i + 2]
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
	if arg == '--test':
		test = True

if sys.argv[-2][0] == '-' and sys.argv[-2][0 : 2] != '--':
	sys.exit('''Error: must specify input file''')
in_file = sys.argv[-1]


# Transformations dictionary for searching reactions
# open transformations worksheet
wb = open_workbook('../data/transformations.xlsx')
transformation_sheet = wb.sheet_by_name('Common chemical relationships')
# Save mz vals and reaction names
mz_list = [x.value for x in transformation_sheet.col(7)[2 : ]]
names = [x.value for x in transformation_sheet.col(0)[2 : ]]
# Save transformations - NOTE dict keys are mz values and the values
# are the reaction names
transformations = dict(zip(mz_list, names))
max_diff = max([abs(x) for x in transformations.keys()])

################################################################################
# Main Script
################################################################################
# Open data file and readlines (ignoring NA lines)
with open(in_file, 'r') as f:
	lines = [line.strip() for line in f if 
				get_mz_in(line).upper() != 'NA' \
				and get_rt_in(line).upper() != 'NA']

# Throw away header line
lines = lines[1 : ]
# Sort lines by mz value (smallest to largest)
lines = sorted(lines, key = lambda line : float(line.split('\t')[2]))
# Testing subsets of the data for timing
if test:
	lines = lines[0 : 500]
# For saving lines of interest
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
		delta_mz = float(get_mz_in(line_inner)) - float(get_mz_in(line_outer))
		if abs(delta_mz) > abs(max_diff) + tolerance:
			if j >= i:
				break
			else:
				if j > j_start:
					j_temp = j
				continue
		if method == get_method_in(line_inner):
			closest_match = min(mz_list, key = \
										 lambda x : min(
										 	abs(x - delta_mz),
										 	abs(x + delta_mz))
										 )
			dist_current = abs(closest_match - delta_mz)
			dist_reverse = abs(closest_match + delta_mz)
			if min(dist_current, dist_reverse) <= tolerance:
				line_to = line_inner
				line_from = line_outer
				if dist_reverse < dist_current:
					line_to = line_outer
					line_from = line_inner
				if method in saved_lines:
					saved_lines[method].append(join_trans_lines(closest_match, 
										 				 line_from,
										 				 line_to,
										 				 transformations,
										 				 delimiter))
				else:
					saved_lines[method] = [join_trans_lines(closest_match,
													 line_from,
													 line_to,
													 transformations,
													 delimiter)]
	j_start = j_temp
num_found_transformations = 0
for method in saved_lines:
	num_found_transformations += len(saved_lines[method])
	# out_file = in_file.split('_')[0].split('.')[0]+'_' + \
	# 	method + '_transformations.csv'
	out_file = in_file.replace('.txt', '_transformations.csv')
	with open(out_file, 'w') as f:
		print(get_header(delimiter), file = f)
		for line in saved_lines[method]:
			print(line, file = f)
	if move_output:
		os.system('mv ' + out_file + ' ' + out_dir)
# summary_file = in_file.split('_')[0].split('.')[0] + '_' + \
	# str(tolerance).replace('.', '-') + '_transformations_summary.txt'
	summary_file = in_file.replace('.txt', '_transformations_summary.txt')
with open(summary_file, 'w') as f:
	print('-----------------------------------------------------------', file=f)
	print('Input file --- ' + in_file, file = f)
	print('System Call --- ' + ' '.join(sys.argv), file = f)
	print('Tolerance (m/z) --- ' + str(tolerance), file = f)
	print('-----------------------------------------------------------', file=f)
	print('*Total*', file = f)
	print('Total Metabolites (no NA) --- ' + str(len(lines)), file = f)
	print('Total found transformations --- ' + \
		str(num_found_transformations), file=f)
	print('', file = f)
	for method in saved_lines:
		print('*' + method + '*', file = f)
		print('Number metabolites (' + method + ') --- ' + \
			str(method_counts[method]), file = f)
		print('Found transformations (' + method + ') --- ' + \
			str(len(saved_lines[method])), file = f)
		print('', file = f)
if move_summary:
	os.system('mv ' + summary_file + ' ' + summary_dir)
elif move_output:
	os.system('mv ' + summary_file + ' ' + out_dir)
end_time = time.time()
print('Total time elapsed - ' + str(end_time - start_time))
