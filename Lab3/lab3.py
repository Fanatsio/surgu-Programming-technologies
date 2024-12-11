class Sort:
    def __init__(self):
        self._steps = []

    def sort(self, data):
        raise NotImplementedError

    def _record_step(self, data):
        self._steps.append(data.copy())

    def get_steps(self):
        return self._steps

class RadixSort(Sort):
    def sort(self, data):
        if not data:
            return data

        if all(isinstance(item, int) for item in data):
            return self._sort_numbers(data)
        elif all(isinstance(item, str) for item in data):
            return self._sort_strings(data)
        else:
            raise ValueError("Input array must contain only integers or only strings.")

    def _sort_numbers(self, data):
        max_num = max(data)
        max_length = len(str(max_num))

        for i in range(max_length):
            buckets = [[] for _ in range(10)]
            for num in data:
                digit = (num // (10 ** i)) % 10
                buckets[digit].append(num)
            data = [num for bucket in buckets for num in bucket]
            self._record_step(data)
        return data

    def _sort_strings(self, data):
        max_length = max(len(item) for item in data)

        for i in range(max_length - 1, -1, -1):
            buckets = [[] for _ in range(256)]
            for item in data:
                key = ord(item[i]) if i < len(item) else 0
                buckets[key].append(item)
            data = [item for bucket in buckets for item in bucket]
            self._record_step(data)
        return data

class SelectionSort(Sort):
    def sort(self, data):
        for i in range(len(data) - 1):
            min_index = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_index]:
                    min_index = j
            data[i], data[min_index] = data[min_index], data[i]
            self._record_step(data)
        return data

class SortWithSteps:
    def __init__(self, sort_algorithm):
        self.sort_algorithm = sort_algorithm

    def sort(self, data):
        return self.sort_algorithm.sort(data)

    def visualize_sorting(self):
        steps = self.sort_algorithm.get_steps()
        for i, step in enumerate(steps, start=1):
            print(f"Step {i}: {', '.join(map(str, step))}")
            print("-" * 20)

def menu():
    print("1 - Сортировка выбором\n"
          "2 - Радикс сортировка\n"
          "0 - Выход")
    return int(input("Введите >> "))

data = [5, 6, 10, 1, 15, 4]
#data = ["michelle", "tigger", "sunshine", "chocolate", "password1", "soccer", "anthony"]

print(f"Массив до сортировки: {data}")

selection_sort = SortWithSteps(SelectionSort())
radix_sort = SortWithSteps(RadixSort())

while True:
    choice = menu()
    if choice == 0:
        print("Выход из программы.")
        break
    elif choice == 1:
        sorted_data = selection_sort.sort(data.copy())
        selection_sort.visualize_sorting()
        print(f"Selection sort result: {sorted_data}")
    elif choice == 2:
        sorted_data = radix_sort.sort(data.copy())
        radix_sort.visualize_sorting()
        print(f"Radix sort result: {sorted_data}")
    else:
        print("Неверный выбор. Попробуйте снова.")
