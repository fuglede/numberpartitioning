from numberpartitioning import complete_greedy, greedy
from numberpartitioning.common import Partition


def test_greedy() -> None:
    numbers = [4, 5, 6, 7, 8]
    expected_partition = [[8], [7, 4], [6, 5]]
    expected_sizes = [8, 11, 11]
    result = greedy(numbers, num_parts=3)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_greedy_can_give_indices() -> None:
    numbers = [4, 5, 6, 7, 8]
    expected_partition = [[4], [3, 0], [2, 1]]
    expected_sizes = [8, 11, 11]
    result = greedy(numbers, num_parts=3, return_indices=True)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_greedy_unordered() -> None:
    numbers = [5, 8, 6, 4, 7]
    expected_partition = [[8], [7, 4], [6, 5]]
    expected_sizes = [8, 11, 11]
    result = greedy(numbers, num_parts=3)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_greedy_unordered_indices() -> None:
    numbers = [5, 8, 6, 4, 7]
    expected_partition = [[1], [4, 3], [2, 0]]
    expected_sizes = [8, 11, 11]
    result = greedy(numbers, num_parts=3, return_indices=True)
    assert result.partition == expected_partition
    assert result.sizes == expected_sizes


def test_greedy_large_problem() -> None:
    numbers = list(range(800, 1200))
    result = greedy(numbers, num_parts=7)
    assert list(map(sum, result.partition)) == result.sizes
    assert max(result.sizes) - min(result.sizes) == 799


def test_complete_greedy_starts_with_greedy_solution() -> None:
    numbers = [4, 5, 6, 7, 8]
    num_parts = 3
    result_greedy = greedy(numbers, num_parts)
    result_complete_greedy = next(complete_greedy(numbers, num_parts))
    assert result_greedy.partition == result_complete_greedy.partition[::-1]
    assert result_greedy.sizes == result_complete_greedy.sizes[::-1]


def test_complete_greedy_starts_with_greedy_solution_indices() -> None:
    numbers = [4, 5, 6, 7, 8]
    num_parts = 3
    result_greedy = greedy(numbers, num_parts, return_indices=True)
    result_complete_greedy = next(
        complete_greedy(numbers, num_parts, return_indices=True)
    )
    assert result_greedy.partition == result_complete_greedy.partition[::-1]
    assert result_greedy.sizes == result_complete_greedy.sizes[::-1]


def test_complete_greedy_starts_with_greedy_solution_large_example() -> None:
    numbers = list(range(800, 1200))
    num_parts = 7
    result_greedy = greedy(numbers, num_parts)
    result_complete_greedy = next(complete_greedy(numbers, num_parts))
    assert result_greedy.partition == result_complete_greedy.partition[::-1]
    assert result_greedy.sizes == result_complete_greedy.sizes[::-1]


def test_complete_greedy_improves() -> None:
    numbers = list(range(20, 30))
    iterator = complete_greedy(numbers, num_parts=3)
    expected_sizes = [19, 18, 16, 14, 13, 11, 10, 9, 7]
    for expected_size in expected_sizes:
        result = next(iterator)
        assert max(result.sizes) - min(result.sizes) == expected_size
        assert sum(result.sizes) == sum(numbers)


def test_complete_greedy_min_objective_gives_different_partitions() -> None:
    def objective(partition: Partition) -> int:
        return min(sum(x) for x in partition)

    numbers = list(range(20, 30))
    iterator = complete_greedy(numbers, num_parts=3, objective=objective)
    expected_variances = [75, 74, 73]
    expected_diffs = [19, 21, 23]
    for expected_variance, expected_diff in zip(expected_variances, expected_diffs):
        result = next(iterator)
        assert expected_variance == objective(result.partition)
        assert expected_diff == max(result.sizes) - min(result.sizes)
