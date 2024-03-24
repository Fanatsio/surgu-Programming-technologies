def menu():
    print("1 - Сортировка выбором\n"
          "2 - Поразрядная сортировка\n"
          "0 - Выход")
    return int(input("Введите >> "))


def selection_sort(arr):
    for i in range(len(arr)):
        min_index = i
        for j in range(i + 1, len(arr)):
            if type(arr[j]) == type(arr[min_index]):
                if arr[j] < arr[min_index]:
                    min_index = j
            elif isinstance(arr[j], int) and isinstance(arr[min_index], str):
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def counting_sort(arr, exp, counts):
    n = len(arr)
    output = [0] * n

    for i in range(n):
        index = ord(arr[i][exp]) if len(arr[i]) > exp else 0
        counts.setdefault(index, 0)
        counts[index] += 1

    sorted_indices = sorted(counts.keys())
    total = 0
    for index in sorted_indices:
        counts[index], total = total, counts[index] + total

    for i in range(n - 1, -1, -1):
        index = ord(arr[i][exp]) if len(arr[i]) > exp else 0
        output[counts[index]] = arr[i]
        counts[index] += 1

    for i in range(n):
        arr[i] = output[i]


def radix_sort(arr):
    max_length = max(len(x) for x in arr)
    for exp in range(max_length - 1, -1, -1):
        counts = {}
        counting_sort(arr, exp, counts)
    return arr
