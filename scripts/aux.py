################################################################################
# Gabe Reder - gkreder@gmail.com
# 08/2017
################################################################################
import math
import time
import sys
################################################################################
# Functions for reading input data files
################################################################################
def get_mz_in(line):
	return line.split('\t')[2]

def get_rt_in(line):
	return line.split('\t')[3]

def get_method_in(line):
	return line.split('\t')[1]

def get_metabolite_in(line):
	return line.split('\t')[0]
################################################################################
# Functions for writing data files
################################################################################
def join_trans_lines(closest_match, line_from, line_to, \
	transformations, delimiter):

	delta_mz_obs = float(get_mz_in(line_to)) - float(get_mz_in(line_from))
	saved_line = [get_metabolite_in(line_from) + '--->' + 
								get_metabolite_in(line_to),
				  transformations[closest_match],
				  str(delta_mz_obs),
				  str(abs(closest_match - delta_mz_obs)),
				  get_metabolite_in(line_from),
				  get_mz_in(line_from),
				  get_rt_in(line_from),
				  get_metabolite_in(line_to),
				  get_mz_in(line_to),
				  get_rt_in(line_to),
				  get_method_in(line_to)]
	return(delimiter.join(saved_line))

def get_header(delimiter):
	return delimiter.join(['transformation',
						   'closest_reaction',
						   'delta_mz_observed',
						   'delta_mz_error',
						   'metabolite_from',
						   'mz_from',
						   'rt_from',
						   'metabolite_to',
						   'mz_to',
						   'rt_to',
						   'method'])

def check_time(i, lines, start_time, tabs = 0):
	index_1 = int(math.ceil((len(lines) / 100)))
	index_10 = int(index_1 * 10)
	index_25 = int(index_1 * 25)
	index_50 = int(index_1 * 50)
	index_75 = int(index_1 * 75)
	index_90 = int(index_1 * 90)
	print_string = ''
	for b in range(tabs):
		print_string += '\t'
	if i == index_1:
		print(print_string + '1% Complete --- ' + 
			  str(time.time() - start_time) + ' seconds elapsed')
		sys.stdout.flush()
	if i == index_10:
		print(print_string + '10% Complete --- ' + 
			  str(time.time() - start_time) + ' seconds elapsed')
		sys.stdout.flush()
	if i == index_25:
		print(print_string + '25% Complete --- ' + 
			  str(time.time() - start_time) + ' seconds elapsed')
		sys.stdout.flush()
	if i == index_50:
		print(print_string + '50% Complete --- ' + 
			  str(time.time() - start_time) + ' seconds elapsed')
		sys.stdout.flush()
	if i == index_75:
		print(print_string + '75% Complete --- ' + 
			  str(time.time() - start_time) + ' seconds elapsed')
		sys.stdout.flush()
	if i == index_90:
		print(print_string + '90% Complete --- ' + 
			  str(time.time() - start_time) + ' seconds elapsed')
		sys.stdout.flush()
################################################################################
# Functions for reading intermediate adduct files
################################################################################
def get_adduct_err(line):
	return float(line.split(',')[3])
def get_adduct_from(line):
	return line.split(',')[0].split('--->')[0]
def get_adduct_to(line):
	return line.split(',')[0].split('--->')[1]
################################################################################
# Functions for reading intermediate trabs files
################################################################################
def get_trans_err(line):
	return float(line.split(',')[3])
def get_trans_from(line):
	return line.split(',')[0].split('--->')[0]
def get_trans_to(line):
	return line.split(',')[0].split('--->')[1]
################################################################################