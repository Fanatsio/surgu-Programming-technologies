import time
import sort


def main():
    array_size = int(input("Введите длину массива >> "))
    array = sort.generate_array(array_size)

    print(f"Сгенерированный массив: {array}")

    while True:
        choice = sort.menu()

        if choice == 0:
            exit()
        elif choice == 1:
            perform_sort(array, sort.select_sort, "сортировки выбором")
        elif choice == 2:
            perform_sort(array, sort.radix_sort_msd, "поразрядной сортировки")


def perform_sort(array, sorting_function, sort_name):
    start_time = time.perf_counter()
    sorting_function(array)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("------------------------------------ \n"
          f"Массив после {sort_name}: {array} \n"
          f"Время выполнения {sort_name}: {elapsed_time} \n"
          "------------------------------------")


if __name__ == "__main__":
    main()
