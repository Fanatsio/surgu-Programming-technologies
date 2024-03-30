import time
import sort_3v as sort

def main():
    with open('sort_benchmark.txt', 'r') as file:
        array = [line.strip() for line in file]

    while True:
        choice = sort.menu()

        if choice == 0:
            exit()
        elif choice == 1:
            perform_sort(array.copy(), sort.insertion_sort, "сортировки вставками")
        elif choice == 2:
            perform_sort(array.copy(), sort.tree_sort, "сортировки бинарным деревом")

def perform_sort(array, sorting_function, sort_name):
    start_time = time.perf_counter()
    sorted_array = sorting_function(array)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    print("------------------------------------\n"
          f"Массив после {sort_name}: {sorted_array}\n"
          f"Длина массива {sort_name}: {len(sorted_array)}\n"
          f"Время выполнения {sort_name}: {elapsed_time}\n"
          f"Является массив отсортированным: {sort.is_sorted(sorted_array)}\n"
          "------------------------------------")

if __name__ == "__main__":
    main()
