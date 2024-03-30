def menu():
    print("1 - Сортировка выбором\n"
          "2 - Поразрядная сортировка\n"
          "0 - Выход")
    return int(input("Введите >> "))


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if isinstance(arr[j], type(arr[min_index])):
                if arr[j] < arr[min_index]:
                    min_index = j
            elif isinstance(arr[j], int) and isinstance(arr[min_index], str):
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 65536

    for i in range(n):
        index = ord(arr[i][exp]) if exp < len(arr[i]) else 0
        count[index] += 1

    for i in range(1, 65536):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = ord(arr[i][exp]) if exp < len(arr[i]) else 0
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    max_len = max(len(s) for s in arr)
    for exp in range(max_len - 1, -1, -1):
        counting_sort(arr, exp)
    return arr
