import time

class Sorting:
    @staticmethod
    def is_sorted(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    def sort(self, arr):
        raise NotImplementedError("Subclasses must implement sort method.")

class SelectionSort(Sorting):
    def sort(self, arr):
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

class RadixSort(Sorting):
    def _counting_sort(self, arr, exp):
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

    def sort(self, arr):
        max_len = max(len(s) for s in arr)
        for exp in range(max_len - 1, -1, -1):
            self._counting_sort(arr, exp)
        return arr

def main():
    with open('sort_benchmark.txt', 'r') as file:
        array = [line.strip() for line in file]

    print(f"Массив до сортировки: {array} \n"
          f"Длина массива: {len(array)}")

    while True:
        choice = menu()

        if choice == 0:
            exit()
        elif choice == 1:
            perform_sort(array.copy(), SelectionSort(), "сортировки выбором")
        elif choice == 2:
            perform_sort(array.copy(), RadixSort(), "поразрядной сортировки")

def perform_sort(array, sorter, sort_name):
    start_time = time.perf_counter()
    sorted_array = sorter.sort(array)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

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

if __name__ == "__main__":
    main()
