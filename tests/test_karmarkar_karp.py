import pytest

from numberpartitioning import karmarkar_karp


def test_karmarkar_karp():
    numbers = [4, 5, 6, 7, 8]
    expected_partition = [[8], [4, 7], [5, 6]]
    expected_sizes = [8, 11, 11]
    result = karmarkar_karp(numbers, num_parts=3)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_karmarkar_karp_can_give_indices():
    numbers = [4, 5, 6, 7, 8]
    expected_partition = [[4], [0, 3], [1, 2]]
    expected_sizes = [8, 11, 11]
    result = karmarkar_karp(numbers, num_parts=3, return_indices=True)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_karmarkar_karp_unordered():
    numbers = [5, 8, 6, 4, 7]
    expected_partition = [[8], [4, 7], [5, 6]]
    expected_sizes = [8, 11, 11]
    result = karmarkar_karp(numbers, num_parts=3)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_karmarkar_karp_unordered_indices():
    numbers = [5, 8, 6, 4, 7]
    expected_partition = [[1], [3, 4], [0, 2]]
    expected_sizes = [8, 11, 11]
    result = karmarkar_karp(numbers, num_parts=3, return_indices=True)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_karmarkar_karp_large_problem():
    numbers = list(range(800, 1200))
    result = karmarkar_karp(numbers, num_parts=7)
    assert list(map(sum, result.partition)) == result.sizes
    assert max(result.sizes) - min(result.sizes) == 603


def test_karmarkar_karp_raises_unsupported_method():
    with pytest.raises(ValueError):
        karmarkar_karp([1, 2, 3], method="foo")
