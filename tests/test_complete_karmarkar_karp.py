from typing import List

import pytest

from numberpartitioning import complete_karmarkar_karp


def _argsort(seq: List[List[int]]) -> List[int]:
    return sorted(range(len(seq)), key=seq.__getitem__)


def test_complete_karmarkar_karp() -> None:
    numbers = [4, 5, 6, 7, 8]
    expected_partitions = [[[4, 7], [5, 6], [8]]]
    expected_sizes = [[11, 11, 8]]
    results = complete_karmarkar_karp(numbers, num_parts=3)
    for i, result in enumerate(results):
        indices = _argsort(result.partition)
        assert [result.partition[i] for i in indices] == expected_partitions[i]
        assert [result.sizes[i] for i in indices] == expected_sizes[i]


def test_complete_karmarkar_karp_can_give_indices() -> None:
    numbers = [4, 5, 6, 7, 8]
    expected_partitions = [[[0, 3], [1, 2], [4]]]
    expected_sizes = [[11, 11, 8]]
    results = complete_karmarkar_karp(numbers, num_parts=3, return_indices=True)
    for i, result in enumerate(results):
        indices = _argsort(result.partition)
        assert [result.partition[i] for i in indices] == expected_partitions[i]
        assert [result.sizes[i] for i in indices] == expected_sizes[i]


def test_complete_karmarkar_karp_unordered() -> None:
    numbers = [5, 8, 6, 4, 7]
    expected_partitions = [[[4, 7], [5, 6], [8]]]
    expected_sizes = [[11, 11, 8]]
    results = complete_karmarkar_karp(numbers, num_parts=3)
    for i, result in enumerate(results):
        indices = _argsort(result.partition)
        assert [result.partition[i] for i in indices] == expected_partitions[i]
        assert [result.sizes[i] for i in indices] == expected_sizes[i]


def test_complete_karmarkar_karp_unordered_indices() -> None:
    numbers = [5, 8, 6, 4, 7]
    expected_partitions = [[[0, 2], [1], [3, 4]]]
    expected_sizes = [[11, 8, 11]]
    results = complete_karmarkar_karp(numbers, num_parts=3, return_indices=True)
    for i, result in enumerate(results):
        indices = _argsort(result.partition)
        assert [result.partition[i] for i in indices] == expected_partitions[i]
        assert [result.sizes[i] for i in indices] == expected_sizes[i]


def test_complete_karmarkar_karp_optimal_solution() -> None:
    numbers = [4, 5, 6, 7, 8]
    expected_partitions = [[[4, 5, 7], [6, 8]], [[4, 5, 6], [7, 8]]]
    expected_sizes = [[16, 14], [15, 15]]
    results = complete_karmarkar_karp(numbers, num_parts=2)
    for i, result in enumerate(results):
        indices = _argsort(result.partition)
        assert [result.partition[i] for i in indices] == expected_partitions[i]
        assert [result.sizes[i] for i in indices] == expected_sizes[i]


def test_complete_karmarkar_karp_larger_example() -> None:
    numbers = list(range(10, 30))
    expected_partitions = [
        [
            [10, 13, 15, 19, 21, 25, 28],
            [11, 12, 16, 18, 22, 24, 27],
            [14, 17, 20, 23, 26, 29],
        ],
        [
            [10, 12, 16, 18, 22, 24, 28],
            [11, 13, 14, 19, 21, 25, 27],
            [15, 17, 20, 23, 26, 29],
        ],
    ]
    expected_sizes = [[131, 130, 129], [130, 130, 130]]
    results = complete_karmarkar_karp(numbers, num_parts=3)
    for i, result in enumerate(results):
        indices = _argsort(result.partition)
        assert [result.partition[i] for i in indices] == expected_partitions[i]
        assert [result.sizes[i] for i in indices] == expected_sizes[i]


def test_complete_karmarkar_karp_no_index_error() -> None:
    numbers = list(range(10, 50))
    results = complete_karmarkar_karp(numbers, num_parts=7)
    expected_partitions = [
        [
            [10, 21, 22, 29, 40, 47],
            [11, 20, 23, 30, 39, 46],
            [12, 19, 24, 31, 38, 45],
            [13, 18, 25, 32, 37, 44],
            [14, 17, 26, 33, 36, 43],
            [15, 28, 35, 41, 49],
            [16, 27, 34, 42, 48],
        ],
        [
            [10, 20, 22, 29, 40, 47],
            [11, 19, 24, 30, 39, 46],
            [12, 18, 25, 31, 38, 45],
            [13, 17, 26, 32, 37, 44],
            [14, 16, 27, 33, 36, 43],
            [15, 28, 35, 41, 49],
            [21, 23, 34, 42, 48],
        ],
    ]
    expected_sizes = [
        [169, 169, 169, 169, 169, 168, 167],
        [168, 169, 169, 169, 169, 168, 168],
    ]
    results = complete_karmarkar_karp(numbers, num_parts=7)
    for i in range(2):
        result = next(results)
        indices = _argsort(result.partition)
        assert [result.partition[i] for i in indices] == expected_partitions[i]
        assert [result.sizes[i] for i in indices] == expected_sizes[i]


def test_complete_karmarkar_karp_raises_unsupported_method() -> None:
    with pytest.raises(ValueError):
        complete_karmarkar_karp([1, 2, 3], method="foo")
