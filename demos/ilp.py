#!python3

""" 
A demo program for finding an optimal partition using ILP.
"""

from numberpartitioning.ilp import *

import logging, sys
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

print("An example from Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.")
walter_numbers = [46, 39, 27, 26, 16, 13, 10]  
print("Min-diff objective:", min_diff_partition(walter_numbers, num_parts=3))
print("Min-max objective:", min_max_partition(walter_numbers, num_parts=3))
print("Max-min objective:", max_min_partition(walter_numbers, num_parts=3))
