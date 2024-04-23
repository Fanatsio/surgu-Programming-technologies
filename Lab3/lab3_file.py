class RadixSort:
    def __init__(self):
        self._steps = []

    def sort(self, data):
        max_length = max(len(str(item)) for item in data)
        for i in range(max_length - 1, -1, -1):
            buckets = [[] for _ in range(256)]
            for item in data:
                key = ord(item[i]) if i < len(item) else 0
                buckets[key].append(item)
            data = []
            for bucket in buckets:
                data.extend(bucket)
            self._steps.append(data.copy())
        return data

class SelectionSort:
    def __init__(self):
        self._steps = []

    def sort(self, data):
        for i in range(len(data)):
            min_index = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_index]:
                    min_index = j
            data[i], data[min_index] = data[min_index], data[i]
            self._steps.append(data.copy())
        return data

class SelectionSortWithSteps(SelectionSort):
    def __init__(self):
        super().__init__()

    def get_steps(self):
        return self._steps
    

class RadixSortWithSteps(RadixSort):
    def __init__(self):
        super().__init__()

    def get_steps(self):
        return self._steps

class SortVisualizer:
    def __init__(self, sort_with_steps):
        self.sort_with_steps = sort_with_steps

    def visualize_sorting(self):
        steps = self.sort_with_steps.get_steps()
        for i, step in enumerate(steps, start=1):
            print(f"Step {i}: \n{','.join(map(str, step))}")

def menu():
    print("1 - Сортировка выбором\n"
          "2 - Поразрядная сортировка\n"
          "0 - Выход")
    return int(input("Введите >> "))

with open('sort_benchmark.txt', 'r') as file:
    data = [line.strip() for line in file]

print(f"Массив до сортировки: {data} \n"
        f"Длина массива: {len(data)}")

while True:
    choice = menu()

    if choice == 0:
        exit()
    elif choice == 1:
        slectionSort = SortWithSteps()
        selected_sorted_data = slectionSort.sort(data.copy())
        # visualizer = SortVisualizer(slectionSort)
        # visualizer.visualize_sorting()

        print(f"sort by me: \n{selected_sorted_data}")
    elif choice == 2:
        radix_sort = SortWithSteps()
        radix_sorted_data = radix_sort.sort(data.copy())
        # visualizer = SortVisualizer(radix_sort)
        # visualizer.visualize_sorting()

        print(f"sort by me: \n{radix_sorted_data}")