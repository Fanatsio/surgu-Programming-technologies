import timeit
from my_list import MyList

# Create a larger sorted list
large_list = MyList(*range(1, 100001))  # List from 1 to 100000

# Function to perform linear search for various positions
def linear_search_test_start():
    large_list.linear_search(1)  # Search for an element at the start

def linear_search_test_middle():
    large_list.linear_search(50000)  # Search for an element in the middle

def linear_search_test_end():
    large_list.linear_search(99999)  # Search for an element near the end

# Function to perform binary search for various positions
def binary_search_test_start():
    large_list.binary_search(1)  # Search for an element at the start

def binary_search_test_middle():
    large_list.binary_search(50000)  # Search for an element in the middle

def binary_search_test_end():
    large_list.binary_search(99999)  # Search for an element near the end

# Measure the time for linear search at different positions
linear_search_time_start = timeit.timeit(linear_search_test_start, number=100)
linear_search_time_middle = timeit.timeit(linear_search_test_middle, number=100)
linear_search_time_end = timeit.timeit(linear_search_test_end, number=100)

# Measure the time for binary search at different positions
binary_search_time_start = timeit.timeit(binary_search_test_start, number=100)
binary_search_time_middle = timeit.timeit(binary_search_test_middle, number=100)
binary_search_time_end = timeit.timeit(binary_search_test_end, number=100)

print(f"Linear search time (start): {linear_search_time_start:.6f} seconds")
print(f"Linear search time (middle): {linear_search_time_middle:.6f} seconds")
print(f"Linear search time (end): {linear_search_time_end:.6f} seconds")

print(f"Binary search time (start): {binary_search_time_start:.6f} seconds")
print(f"Binary search time (middle): {binary_search_time_middle:.6f} seconds")
print(f"Binary search time (end): {binary_search_time_end:.6f} seconds")
#
# Двусвязный кольцевой список не позволяет эффективно использовать бинарный поиск,
# потому что мы не можем напрямую получить доступ к элементу по индексу,
# что приводит к дополнительным затратам времени на перемещение по списку.#