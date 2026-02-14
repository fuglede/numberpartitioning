from numberpartitioning.ilp import *

def test_max_min_partition() -> None:
    # One part:
    result = max_min_partition([10,20,40,0], num_parts=1, return_indices=True)
    assert result == PartitioningResult(partition=[[0, 1, 2, 3]], sizes=[70.0])

    # Two parts:
    result = max_min_partition([10,20,40,0], num_parts=2, return_indices=False)
    assert result == PartitioningResult(partition=[[10, 20, 0], [40]], sizes=[30.0, 40.0])

    # Three parts:
    result = max_min_partition([10,20,40,0], num_parts=3)
    assert int(min(result.sizes)) == 10

    # Four parts:
    result = max_min_partition([10,20,40,0], num_parts=4)
    assert int(min(result.sizes)) == 0

    # More parts than numbers:
    result = max_min_partition([10,20,40,0], num_parts=5)
    assert int(min(result.sizes)) == 0

    # Test multiple copies:
    result = max_min_partition([10,20,40,1], num_parts=2, copies=2, return_indices=True)
    assert result == PartitioningResult(partition=[[0, 1, 2, 3], [0, 1, 2, 3]], sizes=[71.0, 71.0])

    # Test different numbers of copies:
    result = max_min_partition([10,20,40,0], num_parts=2, copies=[2,1,1,0], return_indices=True)
    assert result == PartitioningResult(partition=[[0, 0, 1], [2]], sizes=[40.0, 40.0])

    # Test more than one smallest-part:
    result = max_min_partition([10,20,40,1], num_parts=3, num_smallest_parts=2)
    assert result == PartitioningResult(partition=[[], [10, 20, 1], [40]], sizes=[0.0, 31.0, 40.0])




def test_min_max_partition() -> None:
    # One part:
    result = min_max_partition([10,20,40,0], num_parts=1, return_indices=True)
    assert result == PartitioningResult(partition=[[0, 1, 2, 3]], sizes=[70.0])

    # Two parts:
    result = min_max_partition([10,20,40,0], num_parts=2, return_indices=False)
    assert result == PartitioningResult(partition=[[10, 20], [40, 0]], sizes=[30.0, 40.0])

    # Three parts:
    result = min_max_partition([10,20,40,0], num_parts=3)
    assert int(max(result.sizes)) == 40

    # More parts than numbers:
    result = min_max_partition([10,20,40,0], num_parts=5)
    assert int(max(result.sizes)) == 40

    # Test multiple copies:
    result = min_max_partition([10,20,40,1], num_parts=2, copies=2, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3], [0, 1, 2, 3]], sizes=[71.0, 71.0])

    # Test different numbers of copies:
    result = min_max_partition([10,20,40,0], num_parts=2, copies=[2,1,1,0], return_indices=True)
    assert result == PartitioningResult(partition=[[0, 0, 1], [2]], sizes=[40.0, 40.0])

    # Test more than one largest-part:
    result = min_max_partition([10,20,40,1], num_parts=3, num_largest_parts=2)
    PartitioningResult(partition=[[10, 1], [20], [40]], sizes=[11.0, 20.0, 40.0])




def test_min_diff_partition() -> None:
    # One part:
    result = min_diff_partition([10,20,40,0], num_parts=1, return_indices=True)
    assert result == PartitioningResult(partition=[[0, 1, 2, 3]], sizes=[70.0])

    # Two parts:
    result = min_diff_partition([10,20,40,0], num_parts=2, return_indices=False)
    assert result == PartitioningResult(partition=[[10, 20], [40, 0]], sizes=[30.0, 40.0])

    # Test multiple copies:
    result = min_diff_partition([10,20,40,1], num_parts=2, copies=2, return_indices=True)
    PartitioningResult(partition=[[0, 1, 2, 3], [0, 1, 2, 3]], sizes=[71.0, 71.0])

    # Test different numbers of copies:
    result = min_diff_partition([10,20,40,0], num_parts=2, copies=[2,1,1,0], return_indices=True)
    assert result == PartitioningResult(partition=[[0, 0, 1], [2]], sizes=[40.0, 40.0])
