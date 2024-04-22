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

class RadixSortWithSteps(RadixSort):
    def __init__(self):
        super().__init__()

    def get_steps(self):
        return self._steps

class SortVisualizer:
    def __init__(self, radix_sort_with_steps):
        self.radix_sort_with_steps = radix_sort_with_steps

    def visualize_sorting(self):
        steps = self.radix_sort_with_steps.get_steps()
        for i, step in enumerate(steps, start=1):
            print(f"Step {i}: \n{','.join(map(str, step))}")

radix_sort = RadixSortWithSteps()
data = ["michelle", "tigger", "sunshine", "chocolate", "password1", "soccer", "anthony", 
        "friends", "butterfly", "purple", "angel", "jordan", "liverpool", "justin"]
sorted_data = radix_sort.sort(data)

visualizer = SortVisualizer(radix_sort)
visualizer.visualize_sorting()

print(f"sort by me: \n{sorted_data}")
