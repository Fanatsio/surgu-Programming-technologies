def counting_sort(arr, digit_index):
    count = [0] * 256  # ASCII range
    output = [None] * len(arr)

    for item in arr:
        char = ord(item[digit_index]) if len(item) > digit_index else 0
        count[char] += 1

    for i in range(1, len(count)):
        count[i] += count[i - 1]

    for i in range(len(arr) - 1, -1, -1):
        char = ord(arr[i][digit_index]) if len(arr[i]) > digit_index else 0
        output[count[char] - 1] = arr[i]
        count[char] -= 1

    for i in range(len(arr)):
        arr[i] = output[i]

def msd_radix_sort(arr):
    max_len = max(len(item) for item in arr) if arr else 0
    for i in range(max_len - 1, -1, -1):
        counting_sort(arr, i)
        
def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

with open('sort_benchmark.txt', 'r') as file:
    data_array = []
    for line in file:
        data_array.append(line.strip())

msd_radix_sort(data_array)
print("Sorted array:", data_array)
print("\n\n\n", is_sorted(data_array))
