#!python3

"""
Demonstrates how to use complete algorithms 
such as Complete Greedy.
"""

from numberpartitioning import complete_greedy
numbers = [4, 6, 7, 5, 8]

print("Complete Greedy with k=2:")
for p in complete_greedy(numbers, num_parts=2):
    print (p)

print("Complete Greedy with k=3:")
for p in complete_greedy(numbers, num_parts=3):
    print (p)
