# Assignment 3: Algorithm Efficiency and Scalability

## Overview

This project analyzes the performance of **Randomized Quicksort**, **Deterministic Quicksort**, and a **Hash Table with Chaining**.

The Quicksort implementations are tested using different types of input data to observe how input structure affects performance.

## Files

* `assignment3_algorithms.py` - Python implementation of all algorithms and experiments.
* `quicksort_results.csv` - Results from the Quicksort performance tests.
* `report.md` - Detailed theoretical and empirical analysis.
* `Output Screenshots.png` - Screenshot of the terminal output.
## Algorithms

### Randomized Quicksort

Randomly selects a pivot from the current subarray.

* Expected time: **O(n log n)**
* Worst-case time: **O(n²)**

### Deterministic Quicksort

Uses the first element as the pivot.

* Average-case time: **O(n log n)**
* Worst-case time: **O(n²)**

### Hash Table with Chaining

Uses chaining to handle hash collisions and dynamically resizes when the load factor exceeds 0.75.

Expected performance:

* Insert: **O(1 + α)**
* Search: **O(1 + α)**
* Delete: **O(1 + α)**

where **α** is the load factor.

## Input Distributions

Quicksort was tested with:

* Random arrays
* Sorted arrays
* Reverse-sorted arrays
* Arrays with repeated values

Input sizes ranged from **100 to 5,000 elements**.

## How to Run

```bash
python assignment3_algorithms.py
```

The program tests the algorithms and generates `quicksort_results.csv`.

## Main Findings

Randomized Quicksort showed consistent results on various data structures. Deterministic Quicksort worked efficiently on certain randomized and repeated data structures but had serious difficulties dealing with sorted and reverse-sorted arrays.

When using sorted and reverse-sorted data structures of size more than 1,000, the deterministic version exceeded Python’s recursion depth limit.

The hash table was able to add, search, and delete 10,000 elements, keeping the load factor under control by resizing the array dynamically.

## Conclusion

The experiment proves that theoretical complexity and execution time should both be taken into account. Randomization helps Quicksort algorithm cope better with bad input order, while chaining and dynamic resizing enable efficient operations of hash table despite increasing size of data.