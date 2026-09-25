import random
import time
import csv


# PART 1: RANDOMIZED QUICKSORT
def randomized_partition(my_arr, low, high):
    """Partition using pivot chosen randomly."""
    pivot_idx = random.randint(low, high)

# Move pivot randomly chosen to the end
    my_arr[pivot_idx], my_arr[high] = my_arr[high], my_arr[pivot_idx]

    pivot = my_arr[high]
    i = low - 1

    for j in range(low, high):
        if my_arr[j] <= pivot:
            i += 1
            my_arr[i], my_arr[j] = my_arr[j], my_arr[i]

    my_arr[i + 1], my_arr[high] = my_arr[high], my_arr[i + 1]
    return i + 1


def randomized_quicksort(my_arr, low=0, high=None):
    """In-place Randomized Quicksort."""
    if high is None:
        high = len(my_arr) - 1

    if low < high:
        pivot_position = randomized_partition(my_arr, low, high)

        randomized_quicksort(my_arr, low, pivot_position - 1)
        randomized_quicksort(my_arr, pivot_position + 1, high)

    return my_arr


# PART 1: DETERMINISTIC QUICKSORT
def deterministic_partition(my_arr, low, high):
    """Partition using the first element as the pivot."""
    pivot = my_arr[low]

    i = low + 1
    j = high

    while True:
        while i <= high and my_arr[i] <= pivot:
            i += 1

        while j >= low + 1 and my_arr[j] > pivot:
            j -= 1

        if i >= j:
            break

        my_arr[i], my_arr[j] = my_arr[j], my_arr[i]

    my_arr[low], my_arr[j] = my_arr[j], my_arr[low]
    return j


def deterministic_quicksort(my_arr, low=0, high=None):
    """In-place Quicksort using the first element as pivot."""
    if high is None:
        high = len(my_arr) - 1

    if low < high:
        pivot_position = deterministic_partition(my_arr, low, high)

        deterministic_quicksort(my_arr, low, pivot_position - 1)
        deterministic_quicksort(my_arr, pivot_position + 1, high)

    return my_arr


# PART 2: HASH TABLE WITH CHAINING
class HashTable:
    def __init__(self, initial_capacity=11, max_load_factor=0.75):
        self.capacity = initial_capacity
        self.max_load_factor = max_load_factor
        self.size = 0
        self.table = [[] for _ in range(self.capacity)]

    def _hash(self, key):
        """Polynomial-style hash function for strings and other objects."""
        ky_strng = str(key)
        hash_value = 0
        prime = 31

        for character in ky_strng:
            hash_value = (hash_value * prime + ord(character)) % self.capacity

        return hash_value

    def _load_factor(self):
        return self.size / self.capacity

    def _resize(self):
        old_table = self.table

        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for key, value in bucket:
                self.insert(key, value)

    def insert(self, key, value):
        index = self._hash(key)

        # Update existing key
        for position, (existing_key, existing_value) in enumerate(
            self.table[index]
        ):
            if existing_key == key:
                self.table[index][position] = (key, value)
                return

        # Insert new key-value pair
        self.table[index].append((key, value))
        self.size += 1

        # Resize if load factor becomes too large
        if self._load_factor() > self.max_load_factor:
            self._resize()

    def search(self, key):
        index = self._hash(key)

        for existing_key, value in self.table[index]:
            if existing_key == key:
                return value

        return None

    def delete(self, key):
        index = self._hash(key)

        for position, (existing_key, value) in enumerate(
            self.table[index]
        ):
            if existing_key == key:
                del self.table[index][position]
                self.size -= 1
                return True

        return False

    def __len__(self):
        return self.size


# TESTING
def tst_quicksort():
    tst_cases = [
        [],
        [1],
        [5, 2, 9, 1, 5, 6],
        [1, 1, 1, 1, 1],
        list(range(20)),
        list(range(20, 0, -1))
    ]

    for test in tst_cases:
        expected = sorted(test)

        randomized_result = randomized_quicksort(test.copy())
        deterministic_result = deterministic_quicksort(test.copy())

        assert randomized_result == expected
        assert deterministic_result == expected

    print("Quicksort tests passed.")


def tst_hash_table():
    table = HashTable()

    table.insert("Alice", 95)
    table.insert("Bob", 88)
    table.insert("Charlie", 91)

    assert table.search("Alice") == 95
    assert table.search("Bob") == 88
    assert table.search("Unknown") is None

    table.insert("Alice", 99)
    assert table.search("Alice") == 99

    assert table.delete("Bob") is True
    assert table.search("Bob") is None
    assert table.delete("Unknown") is False

    print("Hash table tests passed.")


# EMPIRICAL PERFORMANCE TESTING
def gen_input(size, distribution):
    if distribution == "random":
        return [random.randint(0, size * 10) for _ in range(size)]

    elif distribution == "sorted":
        return list(range(size))

    elif distribution == "reverse":
        return list(range(size, 0, -1))

    elif distribution == "repeated":
        return [random.randint(0, 9) for _ in range(size)]

    else:
        raise ValueError("Unknown distribution")


def measure_sort(sort_function, data):
    test_data = data.copy()

    start = time.perf_counter()
    sort_function(test_data)
    end = time.perf_counter()

    assert test_data == sorted(data)

    return end - start


def run_benchmark():
    sizes = [100, 500, 1000, 2000, 5000]
    distributions = [
        "random",
        "sorted",
        "reverse",
        "repeated"
    ]

    results = []

    random.seed(42)

    for distribution in distributions:
        for size in sizes:

            data = gen_input(size, distribution)

            # Randomized Quicksort
            randomized_time = measure_sort(
                randomized_quicksort,
                data
            )

            # Deterministic Quicksort
            # Very large sorted or reverse-sorted inputs can lead to
            # recursion issues, so they are handled differently.
            try:
                deterministic_time = measure_sort(
                    deterministic_quicksort,
                    data
                )
            except RecursionError:
                deterministic_time = None

            results.append({
                "distribution": distribution,
                "size": size,
                "randomized_quicksort": randomized_time,
                "deterministic_quicksort": deterministic_time
            })

            print(
                f"{distribution:10} | "
                f"n={size:5} | "
                f"randomized={randomized_time:.6f}s | "
                f"deterministic="
                f"{deterministic_time if deterministic_time is not None else 'RecursionError'}"
            )

    with open("quicksort_results.csv", "w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "distribution",
                "size",
                "randomized_quicksort",
                "deterministic_quicksort"
            ]
        )

        writer.writeheader()
        writer.writerows(results)

    print("\nBenchmark results saved to quicksort_results.csv")


# HASH TABLE TEST
def tst_hash_performance():
    table = HashTable()

    number_of_items = 10000

    start = time.perf_counter()

    for i in range(number_of_items):
        table.insert(f"key_{i}", i)

    insert_time = time.perf_counter() - start

    start = time.perf_counter()

    for i in range(number_of_items):
        table.search(f"key_{i}")

    search_time = time.perf_counter() - start

    start = time.perf_counter()

    for i in range(number_of_items):
        table.delete(f"key_{i}")

    delete_time = time.perf_counter() - start

    print("\nHash Table Performance")
    print("----------------------")
    print(f"Inserted {number_of_items} elements")
    print(f"Total insertion time: {insert_time:.6f} seconds")
    print(f"Total search time:    {search_time:.6f} seconds")
    print(f"Total deletion time:  {delete_time:.6f} seconds")

if __name__ == "__main__":
    tst_quicksort()
    tst_hash_table()
    run_benchmark()
    tst_hash_performance()