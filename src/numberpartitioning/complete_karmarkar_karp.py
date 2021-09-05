import heapq
from dataclasses import dataclass
from itertools import count, permutations
from math import inf
from typing import Iterator, List, Tuple

Partition = Tuple[Tuple[int, ...], ...]

@dataclass
class PartitioningResult:
    """The result of performing a partitioning.

    Parameters
    ----------
    partition:
        The partition as a list of lists; each inner list is a part; a subset of the
        numbers being partitioned so that their disjoint union make up the full set.
    sizes:
        List containing the corresponding sums of the parts; that is, the i'th element
        is the sum of the i'th element of the partition.
    """

    partition: Partition
    sizes: Tuple[int, ...]


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


def _argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)


def _combine_partitions(
        t1: Partition, t2: Partition
        ) -> Iterator[Tuple[Partition, Tuple[int, ...]]]:
    yielded = set()
    for permutation in permutations(t1, len(t1)):
        out = tuple(sorted((tuple(sorted(p + l)) for p, l in zip(permutation, t2))))
        if out not in yielded:
            yielded.add(out)
            yield (out, tuple([sum(x) for x in out]))


def _best_possible_partition_difference(node, num_parts):
    tmp = sorted([sum(subset) for partition in node for subset in partition[2]])
    return -(tmp[-1] - sum(tmp[:-1]) // (num_parts - 1))


def _get_indices(numbers: List[int], partition: Partition) -> Partition:
    indices: List[List[int]] = []
    for p in partition:
        indices.append([])
        for x in p:
            i = numbers.index(x)
            indices[-1].append(i)
            numbers[i] = inf
    return tuple([tuple(x) for x in indices])


def _complete_karmarkar_karp_pure_python(
    numbers: List[int], return_indices: bool, num_parts: int
) -> Iterator[PartitioningResult]:
    stack: List[List[Tuple[int, int, Partition, Tuple[int, ...]]]] = [[]]
    heap_count = count()  # To avoid ambiguity in heaps
    numbers_ = sorted(numbers, reverse=True)
    for i in range(len(numbers_)):
        this_partition: Partition = ((),) * (num_parts - 1) + ((numbers_[i],),)
        this_sizes: Tuple[int, ...] = (0,) * (num_parts - 1) + (numbers_[i],)
        stack[0].append((-numbers_[i], next(heap_count), tuple(this_partition),
            this_sizes))
    visited = set()
    best = -inf
    while stack:
        partitions = stack.pop()
        if _best_possible_partition_difference(partitions, num_parts) <= best:
            continue
        if len(partitions) == 1 and (num := partitions[0][0]) > best:
            best = num
            _, _, final_partition, final_sums = partitions[0]
            if return_indices:
                final_partition = _get_indices(numbers[:], final_partition)
            yield PartitioningResult(final_partition, final_sums)
            if num == 0:
                return
            continue
        if tuple(partitions) not in visited:
            visited.add(tuple(partitions))
        _, _, p1, p1_sum = heapq.heappop(partitions)
        _, _, p2, p2_sum = heapq.heappop(partitions)
        for new_partition, new_sizes in _combine_partitions(p1, p2):
            tmp_partitions = [t for t in partitions]
            indices = _argsort(new_sizes)
            new_sizes = tuple((new_sizes[i] for i in indices))
            new_partition = tuple((new_partition[i] for i in indices))
            diff = new_sizes[-1] - new_sizes[0]
            heapq.heappush(tmp_partitions, (-diff, next(heap_count), new_partition, new_sizes))
            stack.append(tmp_partitions)


METHODS = {"purepython": _complete_karmarkar_karp_pure_python}
