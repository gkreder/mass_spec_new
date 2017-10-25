import os
import sys
scripts_dir = os.path.abspath(os.getcwd())

move_output = False
found_knowns = False
if len(sys.argv) < 2:
	sys.exit('Error: must specify input file')
in_file = sys.argv[-1]
for i, arg in enumerate(sys.argv[1 : -1]):
	if arg == '-o':
		out_dir = sys.argv[i + 2]
		out_dir = os.path.abspath(out_dir)
		move_output = True
	if arg == '-k':
		knowns_file = sys.argv[i + 2]
		found_knowns = True
if not found_knowns:
	sys.exit('Error: must specify knowns file')
if not move_output:
	out_dir = os.path.abspath(scripts_dir + '/../data/output/')
out_dir = os.path.abspath(out_dir)

os.system('mkdir ' + out_dir)

def count_transformations():
	with open(in_file, 'r') as f:
		lines = [x.strip() for x in f.readlines()]
	header = lines[0]
	lines = lines[ 1 : ]
	rxn_counts = {}
	rxn_types = {'known-->known': 0, 'known-->unknown' : 0, 'unknown-->known' : 0, 'unknown-->unknown' : 0}
	transformation_errors = []
	if not os.path.exists(scripts_dir + '/../data/knowns/' + in_file.split('/')[-1].replace('merged.csv', 'knowns.txt')):	
		sys.exit('Error: couldnt find a corresponding knowns file')
	knowns = []
	with open(knowns_file, 'r') as f:
		known_lines = [x.strip() for x in f.readlines()]
		known_lines = known_lines[ 1 : ]
		for k in known_lines:
			knowns.append(k.split('\t')[0])
	with open(out_dir + '/' + in_file.split('/')[-1].replace('merged','known_rxns'), 'w') as f:
		print(header, file = f)
		known_known_lines = [header]
		for line_counter, line in enumerate(lines):
			rxn = line.split(',')[1]
			metab_from = line.split(',')[0].split('--->')[0]
			metab_to= line.split(',')[0].split('--->')[1]
			if metab_from in knowns:
				if metab_to in knowns:
					rxn_types['known-->known'] += 1
					print(line, file = f)
					known_known_lines.append(line)
				else:
					rxn_types['known-->unknown'] += 1
					print(line, file = f)
			else:
				if metab_from in knowns:
					rxn_types['unknown-->known'] += 1
					print(line, file = f)
				else:
					rxn_types['unknown-->unknown'] += 1
			if rxn in rxn_counts:
				rxn_counts[rxn] += 1
			else:
				rxn_counts[rxn] = 1
		

	with open(out_dir + '/' + in_file.split('/')[-1].replace('merged.csv','stats.txt'), 'w') as f:
		print('################################################################################', file = f)
		print('Transformation Counts', file = f)
		print('################################################################################', file = f)
		rxns_sorted = sorted(rxn_counts.items(), key=lambda x:x[1], reverse = True)
		for rxn, count in rxns_sorted:
			print(rxn + ': ' + str(count) + ' (' + "{0:.2f}".format(count / line_counter * 100) + '%)', file = f)
		print('################################################################################', file = f)
		print('Known Reaction Counts', file = f)
		print('################################################################################', file = f)
		for t in rxn_types:
			print(t + ': ' + str(rxn_types[t]) + ' (' + "{0:.2f}".format(rxn_types[t] / line_counter * 100) + '%)', file = f)
	with open(out_dir + '/' + in_file.split('/')[-1].replace('merged', 'known-known-rxns'), 'w') as f:
		for line in known_known_lines:
			print(line, file = f)
count_transformations()
