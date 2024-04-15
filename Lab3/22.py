import matplotlib.pyplot as plt
import matplotlib.animation as animation


class SelectionSortVisualizer:
    def __init__(self, data):
        self.data = data
        self.fig, self.ax = plt.subplots()
        self.ax.set_title('Selection Sort')
        self.bar_rects = self.ax.bar(range(len(data)), [val[0] for val in data], color='lightblue')  # Учитываем только первый элемент каждого подмассива
        self.iteration = 0
        self.iteration_text = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes)
        self.iteration_text.set_text('')
        self.update_frequency = 2000  # Отображаем только каждый десятый шаг сортировки
        
    def selection_sort(self):
        for i in range(len(self.data)):
            min_index = i
            for j in range(i + 1, len(self.data)):
                if self.data[j][0] < self.data[min_index][0]:  # Сравниваем только первые элементы подмассивов
                    min_index = j
            self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
            if i % self.update_frequency == 0:
                yield self.data
            
    def animate(self, frame):
        if self.iteration < len(self.data):
            self.iteration_text.set_text('Iteration: {}'.format(self.iteration))
            for rect, val in zip(self.bar_rects, self.data):
                rect.set_color('lightblue')
            self.bar_rects[self.iteration].set_color('lightcoral')
            self.iteration += 1
            # Обновление высоты столбцов гистограммы после изменения данных
            for rect, val in zip(self.bar_rects, self.data):
                rect.set_height(val[0])  # Используем только первый элемент подмассива
            print(f"Iteration {self.iteration}: {self.data}")  # Вывод текущего состояния массива
        else:
            self.iteration_text.set_text('Sorting completed')
        sorted_array = [''.join(map(chr, sub_arr)) for sub_arr in self.data]
        print(sorted_array)
        return self.bar_rects

    def visualize(self):
        anim = animation.FuncAnimation(self.fig, self.animate, frames=self.selection_sort, interval=10, repeat=False, blit=True)  # Уменьшаем время задержки между кадрами
        plt.show()

def main():
    # Generate random data for visualization
    with open('sort_benchmark.txt', 'r') as file:
        data = [line.strip() for line in file if line.strip()]  # Filter out empty lines
        data = [[ord(char) for char in line] for line in data]

    # Create visualization object
    sorter_visualizer = SelectionSortVisualizer(data.copy())

    # Visualize the sorting process
    sorter_visualizer.visualize()

if __name__ == "__main__":
    main()
