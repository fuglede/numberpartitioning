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


def _argsort(seq: List[int]) -> List[int]:
    return sorted(range(len(seq)), key=seq.__getitem__)


def _combine_partitions(
    t1: Partition, t2: Partition
) -> Iterator[Tuple[Partition, List[int]]]:
    yielded = set()
    for permutation in permutations(t1, len(t1)):
        out_ = tuple(sorted((tuple(sorted(p + l)) for p, l in zip(permutation, t2))))
        out = sorted(sorted(p + l) for p, l in zip(permutation, t2))
        if out_ not in yielded:
            yielded.add(out_)
            yield (out, [sum(x) for x in out])


def _best_possible_partition_difference(
    node: List[Tuple[int, int, Partition, List[int]]], num_parts: int
) -> int:
    tmp = sorted([sum(subset) for partition in node for subset in partition[2]])
    return -(tmp[-1] - sum(tmp[:-1]) // (num_parts - 1))


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
    numbers_ = sorted(numbers, reverse=True)
    for i in range(len(numbers_)):
        l: List[List[int]] = [[] for _ in range(num_parts - 1)]
        r: List[List[int]] = [[numbers_[i]]]
        this_partition: Partition = [*l, *r]
        this_sizes: List[int] = [0] * (num_parts - 1) + [numbers_[i]]
        stack[0].append((-numbers_[i], next(heap_count), this_partition, this_sizes))
    best = -inf
    while stack:
        partitions = stack.pop()
        if _best_possible_partition_difference(partitions, num_parts) <= best:
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
        for new_partition, new_sizes in _combine_partitions(p1, p2):
            tmp_partitions = partitions[:]
            indices = _argsort(new_sizes)
            new_sizes = [new_sizes[i] for i in indices]
            new_partition = [new_partition[i] for i in indices]
            diff = new_sizes[-1] - new_sizes[0]
            heapq.heappush(
                tmp_partitions, (-diff, next(heap_count), new_partition, new_sizes)
            )
            stack.append(tmp_partitions)


METHODS = {"purepython": _complete_karmarkar_karp_pure_python}
