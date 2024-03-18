import random


def menu():
    print("1 - Сортировка выбором \n"
          "2 - Сортировка радикс обмен \n"
          "3 - Сортировка подсчётом \n"
          "4 - Сортировка вставками \n"
          "5 - Сортировка слиянием \n"
          "6 - Сортировка бинарным деревом \n"
          "7 - Сортировка радикс прямая \n"
          "8 - Сортировка пузырьком \n"
          "9 - Быстрая сортировка \n"
          "0 - Выход")
    return int(input("Введите >> "))


def generate_array(array_size):
    return [random.randint(1, 100) for _ in range(array_size)]


def select_sort(sort_array):
    for i in range(len(sort_array) - 1):
        min_index = i
        for k in range(i + 1, len(sort_array)):
            if sort_array[k] < sort_array[min_index]:
                min_index = k
        sort_array[i], sort_array[min_index] = sort_array[min_index], sort_array[i]
    return sort_array


def counting_sorting_lsd(sort_array, exp):
    n = len(sort_array)
    output = [0] * n
    count = [0] * 10

    for num in sort_array:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for num in reversed(sort_array):
        digit = (num // exp) % 10
        output[count[digit] - 1] = num
        count[digit] -= 1

    sort_array[:] = output


def radix_sort_lsd(sort_array):
    max_value = max(sort_array)
    exp = 1
    while max_value // exp > 0:
        counting_sorting_lsd(sort_array, exp)
        exp *= 10
    return sort_array


def counting_sort(array):
    max_val = max(array)
    min_val = min(array)

    count_arr = [0] * (max_val - min_val + 1)

    for num in array:
        count_arr[num - min_val] += 1

    sorted_arr = []
    for i in range(len(count_arr)):
        sorted_arr.extend([i + min_val] * count_arr[i])

    return sorted_arr


def insertion_sort(sort_array):
    for i in range(1, len(sort_array)):
        key = sort_array[i]
        j = i - 1
        while j >= 0 and key < sort_array[j]:
            sort_array[j + 1] = sort_array[j]
            j -= 1
        sort_array[j + 1] = key
    return sort_array


def merge_sort(sort_array):
    if len(sort_array) == 1 or len(sort_array) == 0:
        return sort_array
    left = merge_sort(sort_array[:len(sort_array) // 2])
    right = merge_sort(sort_array[len(sort_array) // 2:])
    n = m = k = 0
    centre = [0] * len(sort_array)
    while n < len(left) and m < len(right):
        if left[n] <= right[m]:
            centre[k] = left[n]
            n += 1
        else:
            centre[k] = right[m]
            m += 1
        k += 1
    while n < len(left):
        centre[k] = left[n]
        n += 1
        k += 1
    while m < len(right):
        centre[k] = right[m]
        m += 1
        k += 1
    for i in range(len(sort_array)):
        sort_array[i] = centre[i]
    return sort_array


class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


def insert(root, key):
    if root is None:
        return Node(key)
    else:
        if root.val < key:
            root.right = insert(root.right, key)
        else:
            root.left = insert(root.left, key)
    return root


def inorder_traversal(root, result):
    if root:
        inorder_traversal(root.left, result)
        result.append(root.val)
        inorder_traversal(root.right, result)


def binary_tree_sort(sort_array):
    root = None
    for element in sort_array:
        root = insert(root, element)

    sorted_result = []
    inorder_traversal(root, sorted_result)
    return sorted_result


def counting_sorting_msd(sort_array, exp):
    n = len(sort_array)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (sort_array[i] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = (sort_array[i] // exp) % 10
        output[count[index] - 1] = sort_array[i]
        count[index] -= 1
        i -= 1

    for i in range(n):
        sort_array[i] = output[i]


def radix_sort_msd(sort_array):
    max_value = max(sort_array)
    exp = 1
    while max_value // exp > 0:
        counting_sorting_msd(sort_array, exp)
        exp *= 10
    return sort_array


def bubble_sort(sort_array):
    n = len(sort_array)
    for i in range(n):
        for j in range(0, n - i - 1):
            if sort_array[j] > sort_array[j + 1]:
                sort_array[j], sort_array[j + 1] = sort_array[j + 1], sort_array[j]
    return sort_array


def quicksort(sort_array):
    if len(sort_array) <= 1:
        return sort_array
    pivot = sort_array[len(sort_array) // 2]
    left = [x for x in sort_array if x < pivot]
    middle = [x for x in sort_array if x == pivot]
    right = [x for x in sort_array if x > pivot]
    return quicksort(left) + middle + quicksort(right)
