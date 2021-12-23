#!python3

from typing import  List, Optional, Callable
from numbers import Number

from numberpartitioning.common import Partition, PartitioningResult

import cvxpy
from numberpartitioning.solve import minimize


def max_min_partition(
    numbers: List[int], num_parts: int = 2, return_indices: bool = False,
    copies = 1, num_smallest_parts:int = 1,
) -> PartitioningResult:
    """
    Produce a partition that maximizes the smallest sum,
    by solving an integer linear program (ILP).
    Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576
    Uses CVXPY as an ILP solver.

    Parameters
    ----------
    numbers
        The list of numbers to be partitioned.
    num_parts
        The desired number of parts in the partition. Default: 2.
    return_indices
        If True, the elements of the parts are the indices of the corresponding entries
        of numbers; if False (default), the elements are the numbers themselves.
    copies
        how many copies are there from each number.
        Can be either a single integer (the same #copies for all numbers),
        or a list of integers (a different #copies for each number).
        Default: 1
    num_smallest_parts
        number of smallest parts whose sum should be maximized.
        Default is 1, which means to just maximize the smallest part-sum.
        A value of 3, for example, means to maximize the sum of the three smallest part-sums.

    Returns
    -------
    A partition represented by a ``PartitioningResult``.

    >>> max_min_partition([10,20,40,0], num_parts=1, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3]], sizes=[70.0])

    >>> max_min_partition([10,20,40,0], num_parts=2, return_indices=False)
    PartitioningResult(partition=[[10, 20, 0], [40]], sizes=[30.0, 40.0])

    >>> result = max_min_partition([10,20,40,0], num_parts=3)
    >>> int(min(result.sizes))
    10

    >>> result = max_min_partition([10,20,40,0], num_parts=4)
    >>> int(min(result.sizes))
    0
    
    >>> result = max_min_partition([10,20,40,0], num_parts=5)
    >>> int(min(result.sizes))
    0
    
    >>> max_min_partition([10,20,40,1], num_parts=2, copies=2, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3], [0, 1, 2, 3]], sizes=[71.0, 71.0])

    >>> max_min_partition([10,20,40,0], num_parts=2, copies=[2,1,1,0], return_indices=True)
    PartitioningResult(partition=[[0, 0, 1], [2]], sizes=[40.0, 40.0])

    >>> max_min_partition([10,20,40,1], num_parts=3, num_smallest_parts=2)
    PartitioningResult(partition=[[], [10, 20, 1], [40]], sizes=[0.0, 31.0, 40.0])
    """
    def minimization_objective(parts_sums):
        return - sum(parts_sums[0:num_smallest_parts])
    return find_optimal_partition(numbers, minimization_objective, num_parts, return_indices, copies)



def min_max_partition(
    numbers: List[int], num_parts: int = 2, return_indices: bool = False,
    copies = 1, num_largest_parts:int = 1,
) -> PartitioningResult:
    """
    Produce a partition that minimizes the largest sum,
    by solving an integer linear program (ILP).

    Parameters
    ----------
    numbers
        The list of numbers to be partitioned.
    num_parts
        The desired number of parts in the partition. Default: 2.
    return_indices
        If True, the elements of the parts are the indices of the corresponding entries
        of numbers; if False (default), the elements are the numbers themselves.
    copies
        how many copies are there from each number.
        Can be either a single integer (the same #copies for all numbers),
        or a list of integers (a different #copies for each number).
        Default: 1
    num_largest_parts
        number of largest parts whose sum should be minimized.
        Default is 1, which means to just minimize the largest part-sum.
        A value of 3, for example, means to minimize the sum of the three largest part-sums.

    Returns
    -------
    A partition represented by a ``PartitioningResult``.

    >>> min_max_partition([10,20,40,0], num_parts=1, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3]], sizes=[70.0])

    >>> min_max_partition([10,20,40,0], num_parts=2, return_indices=False)
    PartitioningResult(partition=[[10, 20], [40, 0]], sizes=[30.0, 40.0])

    >>> result = min_max_partition([10,20,40,0], num_parts=3)
    >>> int(max(result.sizes))
    40
    
    >>> result = min_max_partition([10,20,40,0], num_parts=5)
    >>> int(max(result.sizes))
    40
    
    >>> min_max_partition([10,20,40,1], num_parts=2, copies=2, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3], [0, 1, 2, 3]], sizes=[71.0, 71.0])

    >>> min_max_partition([10,20,40,0], num_parts=2, copies=[2,1,1,0], return_indices=True)
    PartitioningResult(partition=[[0, 0, 1], [2]], sizes=[40.0, 40.0])

    >>> min_max_partition([10,20,40,1], num_parts=3, num_largest_parts=2)
    PartitioningResult(partition=[[10, 1], [20], [40]], sizes=[11.0, 20.0, 40.0])
    """
    def minimization_objective(parts_sums):
        return sum(parts_sums[-num_largest_parts:])
    return find_optimal_partition(numbers, minimization_objective, num_parts, return_indices, copies)


def min_diff_partition(
    numbers: List[int], num_parts: int = 2, return_indices: bool = False,
    copies = 1
) -> PartitioningResult:
    """
    Produce a partition that minimizes the difference between the largest and smallest sum,
    by solving an integer linear program (ILP).

    Parameters
    ----------
    numbers
        The list of numbers to be partitioned.
    num_parts
        The desired number of parts in the partition. Default: 2.
    return_indices
        If True, the elements of the parts are the indices of the corresponding entries
        of numbers; if False (default), the elements are the numbers themselves.
    copies
        how many copies are there from each number.
        Can be either a single integer (the same #copies for all numbers),
        or a list of integers (a different #copies for each number).
        Default: 1

    Returns
    -------
    A partition represented by a ``PartitioningResult``.

    >>> min_diff_partition([10,20,40,0], num_parts=1, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3]], sizes=[70.0])

    >>> min_diff_partition([10,20,40,0], num_parts=2, return_indices=False)
    PartitioningResult(partition=[[10, 20], [40, 0]], sizes=[30.0, 40.0])
    
    >>> min_diff_partition([10,20,40,1], num_parts=2, copies=2, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3], [0, 1, 2, 3]], sizes=[71.0, 71.0])

    >>> min_diff_partition([10,20,40,0], num_parts=2, copies=[2,1,1,0], return_indices=True)
    PartitioningResult(partition=[[0, 0, 1], [2]], sizes=[40.0, 40.0])
    """
    def minimization_objective(parts_sums):
        return parts_sums[-1] - parts_sums[0]
    return find_optimal_partition(numbers, minimization_objective, num_parts, return_indices, copies)


def find_optimal_partition(
    numbers: List[int], 
    minimization_objective: Optional[Callable[[list], float]],
    num_parts: int = 2, return_indices: bool = False,  copies = 1
) -> PartitioningResult:
    """
    Produce a partition that minimizes the given objective,
    by solving an integer linear program (ILP).
    Credit: Rob Pratt, https://or.stackexchange.com/a/6115/2576
    Uses CVXPY as an ILP solver.

    Parameters
    ----------
    numbers
        The list of numbers to be partitioned.
    minimization_objective
        A callable for constructing the objective function to be minimized.
        Gets as input a list of part-sums, sorted from small to large. 
        Each of the part-sums is a cvxpy expression.
        Returns as output an expression that should be minimized.
        See max_min_partition for usage examples.
    num_parts
        The desired number of parts in the partition. Default: 2.
    return_indices
        If True, the elements of the parts are the indices of the corresponding entries
        of numbers; if False (default), the elements are the numbers themselves.
    copies
        how many copies are there from each number.
        Can be either a single integer (the same #copies for all numbers),
        or a list of integers (a different #copies for each number).
        Default: 1

    Returns
    -------
    A partition representing by a ``PartitioningResult``.

    """
    parts = range(num_parts)
    items = range(len(numbers))
    if isinstance(copies, Number):
        copies = [copies]*len(numbers)

    counts:dict = {
        item:
        [cvxpy.Variable(integer=True) for part in parts]
        for item in items
    }	# counts[i][j] determines how many times item i appears in part j.
    parts_sums = [
        sum([counts[item][part]*numbers[item] for item in items])
        for part in parts]

    # Construct the list of constraints:
    constraints = []

    # The counts must be non-negative:
    constraints += [counts[item][part]  >= 0 for part in parts for item in items]

    # Each item must be in exactly one part:
    constraints += [sum([counts[item][part] for part in parts]) == copies[item] for item in items] 	

    # Parts must be in ascending order of their sum (a symmetry-breaker):
    constraints += [parts_sums[part+1] >= parts_sums[part] for part in range(num_parts-1)]

    objective = minimization_objective(parts_sums)
    minimize(objective, constraints)

    partition = [
        sum([int(counts[item][part].value)*[item] 
            for item in items if counts[item][part].value>=1], [])
        for part in parts
    ]
    sums = [parts_sums[part].value for part in parts]
    partition:Partition = [[] for _ in parts]
    for part in parts:
        for item in items:
            count = int(counts[item][part].value)
            if count>=1:
                partition[part] += count * [item if return_indices else numbers[item]]
    return PartitioningResult(partition, sums)




if __name__ == "__main__":
    import doctest
    (failures,tests) = doctest.testmod(report=True)
    print ("{} failures, {} tests".format(failures,tests))
