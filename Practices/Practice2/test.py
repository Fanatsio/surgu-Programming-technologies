import timeit

# Create a larger sorted list as a regular Python list
large_list = list(range(1, 100001))  # List from 1 to 100000

# Function to perform linear search for various positions
def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1

def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Functions to test linear search
def linear_search_test_start():
    linear_search(large_list, 1)  # Search for an element at the start

def linear_search_test_middle():
    linear_search(large_list, 50000)  # Search for an element in the middle

def linear_search_test_end():
    linear_search(large_list, 99999)  # Search for an element near the end

# Functions to test binary search
def binary_search_test_start():
    binary_search(large_list, 1)  # Search for an element at the start

def binary_search_test_middle():
    binary_search(large_list, 50000)  # Search for an element in the middle

def binary_search_test_end():
    binary_search(large_list, 99999)  # Search for an element near the end

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
