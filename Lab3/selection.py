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

class SortVisualizer:
    def __init__(self, slection_sort_with_steps):
        self.slection_sort_with_steps = slection_sort_with_steps

    def visualize_sorting(self):
        steps = self.slection_sort_with_steps.get_steps()
        for i, step in enumerate(steps, start=1):
            print(f"Step {i}: \n{','.join(map(str, step))}")

slectionSort = SelectionSortWithSteps()
data = ["michelle", "tigger", "sunshine", "chocolate", "password1", "soccer", "anthony", 
        "friends", "butterfly", "purple", "angel", "jordan", "liverpool", "justin"]
sorted_data = slectionSort.sort(data)

visualizer = SortVisualizer(slectionSort)
visualizer.visualize_sorting()

print(f"sort by me: \n{sorted_data}")
