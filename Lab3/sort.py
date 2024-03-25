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
            if type(arr[j]) == type(arr[min_index]):
                if arr[j] < arr[min_index]:
                    min_index = j
            elif isinstance(arr[j], int) and isinstance(arr[min_index], str):
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr


def radix_sort(arr):
    pass
