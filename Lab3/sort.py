import random


def menu():
    print("1 - Сортировка выбором \n"
          "2 - Поразрядная сортировка \n"
          "0 - Выход")
    return int(input("Введите >> "))


def generate_array(array_size):
    return [random.randint(1, 100) for _ in range(array_size)]


def select_sort(array):
    for i in range(len(array) - 1):
        min_index = i
        for k in range(i + 1, len(array)):
            if array[k] < array[min_index]:
                min_index = k
        array[i], array[min_index] = array[min_index], array[i]
    return array


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
