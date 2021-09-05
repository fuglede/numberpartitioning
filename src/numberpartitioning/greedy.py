from math import inf
from typing import Callable, Iterator, List, Optional, Tuple

from .common import Partition, PartitioningResult


def greedy(
    numbers: List[int], num_parts: int = 2, return_indices: bool = False
) -> PartitioningResult:
    sorted_numbers = sorted(enumerate(numbers), key=lambda x: x[1], reverse=True)
    sums = [0] * num_parts
    partition: Partition = [[] for _ in range(num_parts)]
    for index, number in sorted_numbers:
        smallest = min(range(len(sums)), key=sums.__getitem__)
        sums[smallest] += number
        partition[smallest].append(index if return_indices else number)
    return PartitioningResult(partition, sums)


def complete_greedy(
    numbers: List[int],
    num_parts: int = 2,
    return_indices: bool = False,
    objective: Optional[Callable[[Partition], float]] = None,
) -> Iterator[PartitioningResult]:
    sorted_numbers = sorted(enumerate(numbers), key=lambda x: x[1], reverse=True)
    # Create a stack whose elements are partitions, their sums, and current depth
    to_visit: List[Tuple[Partition, List[int], int]] = [
        ([[] for _ in range(num_parts)], [0] * num_parts, 0)
    ]
    best_objective_value = inf
    while to_visit:
        partition, sizes, depth = to_visit.pop()
        # If we have reach the leaves of the DFS tree, check if we have an improvement, and
        # yield if we do.
        if depth == len(numbers):
            new_objective_value = (
                objective(partition) if objective else max(sizes) - min(sizes)
            )
            if new_objective_value < best_objective_value:
                best_objective_value = new_objective_value
                yield PartitioningResult(partition, sizes)
        else:
            index, number = sorted_numbers[depth]
            # Order parts by decreasing size, so smallest part ends up on top of stack.
            for part_index in sorted(
                range(len(sizes)), key=sizes.__getitem__, reverse=True
            ):
                # Create the next vertex; be careful to copy lists when necessary, but
                # note that we can reuse all but one part in the existing partition.
                new_partition = list(partition)
                new_partition[part_index] = list(new_partition[part_index]) + [
                    index if return_indices else number
                ]
                new_sizes = list(sizes)
                new_sizes[part_index] += number
                new_depth = depth + 1
                to_visit.append((new_partition, new_sizes, new_depth))
