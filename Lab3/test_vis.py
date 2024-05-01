import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class SelectionSortVisualizer:
    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Selection Sort')
        self.bar_rects = self.ax.bar(range(len(data)), data, color='lightblue')
        self.iteration = 0
        self.iteration_text = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes)

    def selection_sort(self):
        for i in range(len(self.data)):
            min_index = i
            for j in range(i + 1, len(self.data)):
                if self.data[j] < self.data[min_index]:
                    min_index = j
            self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
            yield self.data

    def animate(self, frame):
        print(f"Current iteration: {self.iteration}, Length of data: {len(self.data)}")
        if self.iteration < len(self.data):
            self.iteration_text.set_text(f'Iteration: {self.iteration}')
            self.bar_rects[self.iteration].set_color('lightcoral')
            self.iteration += 1
            for rect, val in zip(self.bar_rects, self.data):
                rect.set_height(val)
            print(f"Iteration {self.iteration}: {self.data}")  # Print data after each iteration
        else:
            self.iteration_text.set_text('Sorting completed')
            self.bar_rects[-1].set_color('lightcoral')  # Highlight the last element
        return self.bar_rects

    def visualize(self):
        anim = animation.FuncAnimation(self.fig, self.animate, frames=self.selection_sort, repeat=False, blit=True)
        plt.show()

np.random.seed(0)
data = np.random.randint(1, 100, size=100)

sorter_visualizer = SelectionSortVisualizer(data.copy())
sorter_visualizer.visualize()
