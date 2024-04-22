import time
import random

class Sorting:
    @staticmethod
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def sort(self, arr):
        raise NotImplementedError("Subclasses must implement sort method.")


class SelectionSort(Sorting):
    @staticmethod
    def sort(arr):
        steps = []
        for i in range(len(arr)):
            min_index = i
            for j in range(i + 1, len(arr)):
                if arr[j] < arr[min_index]:
                    min_index = j
            arr[i], arr[min_index] = arr[min_index], arr[i]
            steps.append(arr.copy())
        return arr, steps


class RadixSort(Sorting):
    @staticmethod
    def counting_sort(arr, exp):
        n = len(arr)
        output = [0] * n
        count = [0] * 10

        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        for i in range(1, 10):
            count[i] += count[i - 1]

        i = n - 1
        while i >= 0:
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1
            i -= 1

        for i in range(n):
            arr[i] = output[i]

    @staticmethod
    def sort(arr):
        steps = []
        max_num = max(arr)
        exp = 1
        while max_num // exp > 0:
            RadixSort.counting_sort(arr, exp)
            steps.append(arr.copy())
            exp *= 10
        return arr, steps

# class RadixSort:
#     def __init__(self) -> None:
#         self._steps = []
        
#     def sort(self, data):
        


def perform_sort(array, sort_func, sort_name):
    start_time = time.perf_counter()
    sorted_array, steps = sort_func(array)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("------------------------------------\n")
    for step in steps:
        print(step)
    print("------------------------------------\n"
          f"Массив после {sort_name}: {sorted_array}\n"
          f"Длина массива {sort_name}: {len(sorted_array)}\n"
          f"Время выполнения {sort_name}: {elapsed_time}\n"
          f"Является массив отсортированным: {Sorting.is_sorted(sorted_array)}\n")


def menu():
    print("1 - Сортировка выбором\n"
          "2 - Поразрядная сортировка\n"
          "0 - Выход")
    return int(input("Введите >> "))


def main():
    array = [random.randint(1, 100) for _ in range(10)]

    print(f"Массив до сортировки: {array} \n"
          f"Длина массива: {len(array)}")

    while True:
        choice = menu()

        if choice == 0:
            exit()
        elif choice == 1:
            perform_sort(array.copy(), SelectionSort.sort, "сортировки выбором")
        elif choice == 2:
            perform_sort(array.copy(), RadixSort.sort, "поразрядной сортировки")


if __name__ == "__main__":
    main()
