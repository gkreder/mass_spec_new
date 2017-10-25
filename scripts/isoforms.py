import sys
import os
# from xlrd import open_workbook
from aux import *
import time
start_time = time.time()
################################################################################
# Parameters
################################################################################
delimiter = ','
mz_tolerance = 0.0005
################################################################################
# Read Input Arguments
################################################################################
test = False
move_output = False
if len(sys.argv) < 2:
	sys.exit('''\t Error: must specify input file
				USAGE: python fragments_adducts.py [args] input_file
				args:
					-o: output directory
					-t: mz tolerance (default 0.0005) ''')
for i, arg in enumerate(sys.argv[1 : -1]):
	if arg[0] == '-':
		if sys.argv[i + 2][0] == '-' or i == len(sys.argv[1 : -1]) - 1:
			if arg[0 : 2] != '--':
				sys.exit('Error: Hanging argument flag')
	if arg == '-t':
		tolerance = float(sys.argv[i + 2])
	if arg == '-o':
		out_dir = sys.argv[i + 2]
		out_dir = os.path.abspath(out_dir)
		if out_dir[-1] != '/':
			out_dir = out_dir + '/'
		move_output = True
	if arg == '--test':
		test = True
if sys.argv[-2][0] == '-' and sys.argv[-2][0 : 2] != '--':
	sys.exit('''Error: must specify input file''')
in_file = sys.argv[-1]
################################################################################
# Main Script
################################################################################
# open input file and grab data (ignoring NA lines)
with open(in_file, 'r') as f:
	lines = [line.strip() for line in f if \
				get_mz_in(line).upper() != 'NA'\
				and get_rt_in(line).upper() != 'NA']
# Throw away header line
lines = lines[ 1 : ]
# Sort lines by mz value (smallest to largest)
lines = sorted(lines, key = lambda line : float(line.split('\t')[2]))
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
		# delta_rt = float(get_rt_in(line_inner)) - float(get_rt_in(line_outer))
		delta_mz = float(get_mz_in(line_inner)) - float(get_mz_in(line_outer))
		if abs(delta_mz) > mz_tolerance:
			if j >= i:
				break
			else:
				if j > j_start:
					j_temp = j
				continue
		if i == j:
			continue
		if method == get_method_in(line_inner):
			closest_match = 'isoform'
			line_to = line_inner
			line_from = line_outer
			# if dist_reverse < dist_current:
			# 	line_to = line_outer
			# 	line_from = line_inner
			if method in saved_lines:
				saved_lines[method].append(join_trans_lines(delta_mz,
													line_from,
									 				line_to,
									 				{delta_mz : 'isoform'},
									 				','))
			else:
				saved_lines[method] = [join_trans_lines(delta_mz,
												line_from,
												line_to,
												{delta_mz : 'isoform'},
												',')]
	j_start = j_temp
num_found_isoforms = 0
for method in saved_lines:
	num_found_isoforms += len(saved_lines[method])
	out_file = in_file.replace('.txt', '_isoforms.csv')
	with open(out_file, 'w') as f:
		print(get_header(','), file = f)
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
		+ '_isoforms.csv'
	with open(out_file, 'w') as f:
		print(get_header(','), file = f)
print('-----------------------------------------------------------')
print('Input file --- ' + in_file)
print('System Call --- ' + ' '.join(sys.argv))
print('Tolerance (mz) --- ' + str(mz_tolerance))
print('-----------------------------------------------------------')
print('*Total*')
print('Total Metabolites (no NA) --- ' + str(len(lines)))
print('Total found isoforms --- ' + \
	str(num_found_isoforms))
print('')
for method in saved_lines:
	print('*' + method + '*')
	print('Number metabolites (' + method + ') --- ' + \
		str(method_counts[method]))
	print('Found isoforms (' + method + ') --- ' + \
		str(len(saved_lines[method])))
	print('')
end_time = time.time()
print('Total time elapsed - ' + str(end_time - start_time))