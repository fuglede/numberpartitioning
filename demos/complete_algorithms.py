#!python3

"""
Demonstrates how to use complete algorithms 
such as Complete Greedy.
"""

from numberpartitioning import complete_greedy

print("Complete Greedy with k=2, default objective:")
for p in complete_greedy([4, 6, 7, 5, 8], num_parts=2):
    print (p)

# Define different objectives (all of them for minimization)
def largest_sum(partition):
    return max([sum(part) for part in partition])
def minus_smallest_sum(partition):
    return -min([sum(part) for part in partition])
def largest_diff(partition):
    sums = [sum(part) for part in partition]
    return max(sums)-min(sums)

print("An example from Walter (2013), 'Comparing the minimum completion times of two longest-first scheduling-heuristics'.")
walter_numbers = [46, 39, 27, 26, 16, 13, 10]  
print("Complete Greedy with k=3, min-diff objective (default):")
for p in complete_greedy(walter_numbers, num_parts=3):
    print (p)
print("Complete Greedy with k=3, min-max objective:")
for p in complete_greedy(walter_numbers, num_parts=3, objective=largest_sum):
    print (p)
print("Complete Greedy with k=3, max-min objective:")
for p in complete_greedy(walter_numbers, num_parts=3, objective=minus_smallest_sum):
    print (p)
