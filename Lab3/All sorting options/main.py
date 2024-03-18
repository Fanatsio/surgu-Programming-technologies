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
            perform_sort(array, sort.radix_sort_lsd, "сортировки радикс обмен")
        elif choice == 3:
            perform_sort(array, sort.counting_sort, "сортировки подсчётом")
        elif choice == 4:
            perform_sort(array, sort.insertion_sort, "сортировки вставками")
        elif choice == 5:
            perform_sort(array, sort.merge_sort, "сортировки слиянием")
        elif choice == 6:
            perform_sort(array, sort.binary_tree_sort, "сортировки бинарным деревом")
        elif choice == 7:
            perform_sort(array, sort.radix_sort_msd, "сортировки радикс прямая")
        elif choice == 8:
            perform_sort(array, sort.bubble_sort, "сортировки пузырьком")
        elif choice == 9:
            perform_sort(array, sort.quicksort, "быстрой сортировки")


def perform_sort(array, sorting_function, sort_name):
    start_time = time.perf_counter()
    sorted_arr = sorting_function(array)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("------------------------------------ \n"
          f"Массив после {sort_name}: {sorted_arr} \n"
          f"Время выполнения {sort_name}: {elapsed_time} \n"
          "------------------------------------")


if __name__ == "__main__":
    main()
