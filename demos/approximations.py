#!python3

"""
Demonstrates how to use approximation algorithms 
such as Karmarkar-Karp and Greedy.
"""

from numberpartitioning import karmarkar_karp, greedy, complete_greedy
numbers = [4, 6, 7, 5, 8]
print("Karmarkar-Karp with k=2", karmarkar_karp(numbers, num_parts=2))
print("Karmarkar-Karp with k=3", karmarkar_karp(numbers, num_parts=3))
print("Greedy with k=2", greedy(numbers, num_parts=2))
print("Greedy with k=3", greedy(numbers, num_parts=3))
print("Complete Greedy with k=2", complete_greedy(numbers, num_parts=2))
print("Complete Greedy with k=3", complete_greedy(numbers, num_parts=3))
