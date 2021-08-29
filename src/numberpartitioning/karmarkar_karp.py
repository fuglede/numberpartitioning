import heapq
from dataclasses import dataclass
from itertools import count
from typing import List, Tuple

Partition = List[List[int]]


@dataclass
class PartitioningResult:
    partition: Partition
    sizes: List[int]


def karmarkar_karp(
    numbers: List[int],
    num_parts: int = 2,
    return_indices: bool = False,
    method: str = "purepython",
) -> PartitioningResult:
    if method not in METHODS:
        raise ValueError(
            f'Invalid method "{method}". Valid options: {", ".join(METHODS)}'
        )
    return METHODS[method](numbers, return_indices, num_parts)


def _argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)


def _karmarkar_karp_pure_python(
    numbers: List[int], return_indices: bool, num_parts: int
) -> PartitioningResult:
    partitions: List[Tuple[int, int, Partition, List[int]]] = []
    heap_count = count()  # To avoid ambiguity in heap
    for i in range(len(numbers)):
        this_partition: Partition = []
        for n in range(num_parts - 1):
            this_partition.append([])
        this_partition.append([i if return_indices else numbers[i]])
        this_sizes: List[int] = [0] * (num_parts - 1) + [numbers[i]]
        heapq.heappush(
            partitions, (-numbers[i], next(heap_count), this_partition, this_sizes)
        )
    for k in range(len(numbers) - 1):
        _, _, p1, p1_sum = heapq.heappop(partitions)
        _, _, p2, p2_sum = heapq.heappop(partitions)
        new_sizes: List[int] = [
            p1_sum[j] + p2_sum[num_parts - j - 1] for j in range(num_parts)
        ]
        new_partition: Partition = [
            p1[j] + p2[num_parts - j - 1] for j in range(num_parts)
        ]
        indices = _argsort(new_sizes)
        new_sizes = [new_sizes[i] for i in indices]
        new_partition = [new_partition[i] for i in indices]
        diff = new_sizes[-1] - new_sizes[0]
        heapq.heappush(partitions, (-diff, next(heap_count), new_partition, new_sizes))
    _, _, final_partition, final_sums = partitions[0]
    return PartitioningResult(final_partition, final_sums)


METHODS = {"purepython": _karmarkar_karp_pure_python}
