import heapq
from itertools import count, permutations
from math import inf
from typing import Iterator, List, Tuple

from .common import Partition, PartitioningResult


def complete_karmarkar_karp(
    numbers: List[int],
    num_parts: int = 2,
    return_indices: bool = False,
    method: str = "purepython",
) -> Iterator[PartitioningResult]:
    """Produce partitions using the complete Karmarkar--Karp algorithm.

    Parameters
    ----------
    numbers
        The list of numbers to be partitioned.
    num_parts
        The desired number of parts in the partition. Default: 2.
    return_indices
        If True, the elements of the parts are the indices of the corresponding entries
        of numbers; if False (default), the elements are the numbers themselves.
    method
        Which specific implementation to use. Currently the only allowed (and default)
        value is "purepython".

    Returns
    -------
    An iterator yielding partitions represented by ``PartitioningResult`` of
    increasing quality until an optimal partition is found.

    """
    if method not in METHODS:
        raise ValueError(
            f'Invalid method "{method}". Valid options: {", ".join(METHODS)}'
        )
    return METHODS[method](numbers, return_indices, num_parts)


def _combine_partitions(
    partition_1: Partition, partition_2: Partition
) -> Iterator[Tuple[Partition, List[int]]]:
    yielded = set()
    for permutation in permutations(partition_1, len(partition_1)):
        out = sorted(sorted(p + l) for p, l in zip(permutation, partition_2))
        out_ = tuple(tuple(el) for el in out)
        if out_ not in yielded:
            yielded.add(out_)
            yield (out, [sum(x) for x in out])


def _possible_partition_difference_lower_bound(
    node: List[Tuple[int, int, Partition, List[int]]], num_parts: int
) -> int:
    sizes_flattened = [size for partition in node for size in partition[3]]
    max_sizes_flattened = max(sizes_flattened)
    return -(
        max_sizes_flattened
        - (sum(sizes_flattened) - max_sizes_flattened) // (num_parts - 1)
    )


def _get_indices(numbers: List[int], partition: Partition) -> Partition:
    large_number = max(numbers) + 1
    indices: List[List[int]] = []
    for subpartition in partition:
        indices.append([])
        for x in subpartition:
            i = numbers.index(x)
            indices[-1].append(i)
            numbers[i] = large_number
    return indices


def _complete_karmarkar_karp_pure_python(
    numbers: List[int], return_indices: bool, num_parts: int
) -> Iterator[PartitioningResult]:
    stack: List[List[Tuple[int, int, Partition, List[int]]]] = [[]]
    heap_count = count()  # To avoid ambiguity in heaps
    for number in numbers:
        l: List[List[int]] = [[] for _ in range(num_parts - 1)]
        r: List[List[int]] = [[number]]
        this_partition: Partition = l + r
        this_sizes: List[int] = [0] * (num_parts - 1) + [number]
        heapq.heappush(
            stack[0], (-number, next(heap_count), this_partition, this_sizes)
        )
    best = -inf
    while stack:
        partitions = stack.pop()
        if _possible_partition_difference_lower_bound(partitions, num_parts) <= best:
            continue
        if len(partitions) == 1:
            num = partitions[0][0]
            if num > best:
                best = num
                _, _, final_partition, final_sums = partitions[0]
                if return_indices:
                    final_partition = _get_indices(numbers[:], final_partition)
                yield PartitioningResult(final_partition, final_sums)
                if num == 0:
                    return
            continue
        _, _, p1, p1_sum = heapq.heappop(partitions)
        _, _, p2, p2_sum = heapq.heappop(partitions)
        tmp_stack_extension = []
        for new_partition, new_sizes in _combine_partitions(p1, p2):
            tmp_partitions = partitions[:]
            diff = max(new_sizes) - min(new_sizes)
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_partition, new_sizes)
            )
            tmp_stack_extension.append(tmp_partitions)
        stack.extend(sorted(tmp_stack_extension))


METHODS = {"purepython": _complete_karmarkar_karp_pure_python}
