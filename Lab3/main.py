import time
import sort


def main():
    with open('sort_benchmark.txt', 'r') as file:
        array = file.readlines()

    print(f"Сгенерированный массив: {array} \n"
          f"Длина массива до сортировки: {len(array)}")

    while True:
        choice = sort.menu()

        if choice == 0:
            exit()
        elif choice == 1:
            perform_sort(array.copy(), sort.selection_sort, "сортировки выбором")
        elif choice == 2:
            perform_sort(array.copy(), sort.radix_sort, "поразрядной сортировки")


def perform_sort(array, sorting_function, sort_name):
    start_time = time.perf_counter()
    sorted_array = sorting_function(array)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("------------------------------------\n"
          f"Массив после {sort_name}: {sorted_array}\n"
          f"Длина массива после {sort_name}: {len(sorted_array)}\n"
          f"Время выполнения {sort_name}: {elapsed_time}\n"
          "------------------------------------")


if __name__ == "__main__":
    main()
