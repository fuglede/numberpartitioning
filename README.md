# Partition problem solvers in Python

This repository includes an implementation of the [Karmarkar--Karp algorithm](https://en.wikipedia.org/wiki/Largest_differencing_method) (also known as the largest differencing method) for the [multiway number partitioning optimization problem](https://en.wikipedia.org/wiki/Multiway_number_partitioning), as well as some greedy algorithms.

## The problem

Concretely, the problem we solve is the following: Suppose *S* is some collection of integers, and *k* is some positive integer, find a partition of *S* into *k* parts so that the sums of the integers in each part are as close as possible.

The objective function describing "closeness" is usually taken to be the difference between the largest and smallest sum among all parts. The optimization version is NP-hard, and the bundled algorithm only aims to provide a good solution in short time. This also means that they can be useful for other objective functions such as, say, the variance of all sums.

## Installation

The package is available from [PyPI](https://pypi.org/project/numberpartitioning/):

```sh
pip install numberpartitioning
```

It can also be obtained from [conda-forge](https://anaconda.org/conda-forge/numberpartitioning):

```sh
mamba install -c conda-forge numberpartitioning
```

## Examples

Suppose we want to split the collection `[4, 6, 7, 5, 8]` into three parts. We can achieve that as follows:

```python
from numberpartitioning import karmarkar_karp
numbers = [4, 6, 7, 5, 8]
result = karmarkar_karp(numbers, num_parts=3)
```

Here, `result.partition` becomes `[[8], [4, 7], [5, 6]]`, and `result.sizes` are the sums of each part, `[8, 11, 11]`. This happens to be optimal.

As noted [on Wikipedia](https://en.wikipedia.org/wiki/Largest_differencing_method), an example where this approach does not give the optimal result is the following:

```python
from numberpartitioning import karmarkar_karp
numbers = [5, 5, 5, 4, 4, 3, 3, 1]
result = karmarkar_karp(numbers, num_parts=3)
```

Here, `result.sizes` is `[9, 10, 11]` but it is possible to achieve a solution in which the sums of each part is 10.
