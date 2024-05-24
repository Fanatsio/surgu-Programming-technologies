from list_node import ListNode

class MyList:
    def __init__(self, *args):
        self.head = None
        self.tail = None
        self._count = 0

        for arg in args:
            self.append(arg)

    def append(self, value):
        new_node = ListNode(value)
        if not self.head:
            self.head = self.tail = new_node
            new_node.next = new_node.prev = new_node
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node
        self._count += 1

    def __len__(self):
        return self._count

    def __str__(self):
        if not self.head:
            return "Empty"
        result = ""
        current = self.head
        for _ in range(self._count):
            result += str(current) + " -> "
            current = current.next
        return result + "(back to head)"

    def remove(self, value):
        if not self.head:
            raise ValueError("List is empty")
        current = self.head
        for _ in range(self._count):
            if current.value == value:
                if self._count == 1:
                    self.head = self.tail = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                    if current == self.head:
                        self.head = current.next
                    elif current == self.tail:
                        self.tail = current.prev
                self._count -= 1
                return
            current = current.next
        raise ValueError(f"{value} not found in list")

    def insert(self, index, value):
        if index < 0 or index > self._count:
            raise IndexError("Index out of bounds")

        if index == 0:
            self.prepend(value)
        elif index == self._count:
            self.append(value)
        else:
            current = self.head
            for _ in range(index):
                current = current.next
            new_node = ListNode(value, current.prev, current)
            current.prev.next = new_node
            current.prev = new_node
            self._count += 1

    def prepend(self, value):
        self.append(value)
        self.head = self.head.prev

    def pop(self):
        if not self.head:
            raise IndexError('pop from empty list')
        
        value = self.tail.value
        if self._count == 1:
            self.head = self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = self.head
            self.head.prev = self.tail
        self._count -= 1
        return value

    def clear(self):
        self.head = None
        self.tail = None
        self._count = 0

    def extend(self, other):
        if not isinstance(other, MyList):
            raise TypeError("other must be MyList")
        
        current = other.head
        if current:
            for _ in range(len(other)):
                self.append(current.value)
                current = current.next

    def copy(self):
        new_list = MyList()
        current = self.head
        if current:
            for _ in range(self._count):
                new_list.append(current.value)
                current = current.next
        return new_list

    def index(self, value):
        current = self.head
        for i in range(self._count):
            if current.value == value:
                return i
            current = current.next
        raise ValueError(f"{value} is not in list")

    def count(self, value):
        count = 0
        current = self.head
        for _ in range(self._count):
            if current.value == value:
                count += 1
            current = current.next
        return count

    def reverse(self):
        current = self.head
        if current:
            for _ in range(self._count):
                current.prev, current.next = current.next, current.prev
                current = current.prev  # переход к следующему элементу, который теперь является предыдущим
            self.head, self.tail = self.tail, self.head

    def sort(self):
        if self._count < 1:
            return  # Если в списке меньше 1 элементов, сортировка не требуется

        def insertion_sort(head):
            sorted_tail = head  # Указатель на конец отсортированной части списка
            current = head.next  # Текущий узел для вставки
            while current != head:  # Пока не вернулись к начальному узлу
                next_node = current.next  # Сохраняем следующий узел
                if current.value < sorted_tail.value:  # Если текущий узел меньше последнего отсортированного узла
                    sorted_tail.next = current.next  # Исключаем текущий узел из списка
                    current.next.prev = sorted_tail
                    if current.value < head.value:  # Если текущий узел меньше головы списка
                        current.prev = head.prev
                        current.next = head
                        head.prev.next = current
                        head.prev = current
                        head = current  # Обновляем голову списка
                    else:
                        search = head
                        while search.next.value < current.value:  # Поиск позиции для вставки
                            search = search.next
                        current.prev = search
                        current.next = search.next
                        search.next.prev = current
                        search.next = current  # Вставляем текущий узел на правильную позицию
                else:
                    sorted_tail = current  # Обновляем конец отсортированной части списка
                current = next_node  # Переходим к следующему узлу
            return head  # Возвращаем обновленную голову списка

        self.head = insertion_sort(self.head)
        # Обновляем ссылку на хвост списка
        self.tail = self.head.prev


    def linear_search(self, target, key=lambda x: x):
        current = self.head
        if not current:
            return None  # Если список пуст, возвращаем None
        for _ in range(self._count):
            if key(current.value) == target:  # Если значение текущего узла равно искомому
                return current  # Возвращаем текущий узел
            current = current.next  # Переходим к следующему узлу
        return None  # Если искомое значение не найдено, возвращаем None


    def binary_search(self, target, key=lambda x: x):
        if not self.head:
            return -1  # Если список пуст, возвращаем -1
        # Преобразуем циклический связанный список в обычный список
        arr = []
        current = self.head
        for _ in range(self._count):
            arr.append(current.value)
            current = current.next
        # Выполняем бинарный поиск в обычном списке
        left, right = 0, len(arr) - 1
        while left <= right:
            mid = (left + right) // 2
            if key(arr[mid]) == target:
                return mid  # Возвращаем индекс найденного элемента
            elif key(arr[mid]) < target:
                left = mid + 1  # Ищем в правой половине
            else:
                right = mid - 1  # Ищем в левой половине
        return -1  # Если элемент не найден, возвращаем -1
