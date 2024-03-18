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


def counting_sort(array, exp):
    n = len(array)
    output = [0] * n
    count = [0] * 10

    for num in array:
        digit = (num // exp) % 10
        count[digit] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for num in reversed(array):
        digit = (num // exp) % 10
        output[count[digit] - 1] = num
        count[digit] -= 1

    array[:] = output


def radix_sort(array):
    max_value = max(array)
    exp = 1
    while max_value // exp > 0:
        counting_sort(array, exp)
        exp *= 10
