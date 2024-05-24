from list_node import ListNode

class MyList:
    def __init__(self, *args):
        """
        Конструктор списка. Может принимать 0 или 1 аргумент (начальное значение).
        """
        if args and args[0] is not None:  # Если передан аргумент и он не None
            x = ListNode(args[0])  # Создаём узел с переданным значением
            self.head = x  # Устанавливаем голову списка
            self._count = 1  # Устанавливаем количество элементов в списке
        else:
            self.head = None  # Голова списка пустая
            self._count = 0  # Список пустой

    def append(self, value):
        """
        Добавляет элемент в конец списка.
        """
        if self.head:  # Если список не пустой
            a = self.head  # Начинаем с головы списка
            while a.next:  # Проходим по списку до последнего элемента
                a = a.next
            a.next = ListNode(value)  # Добавляем новый узел в конец
        else:  # Если список пустой
            self.head = ListNode(value)  # Создаём новый узел и делаем его головой списка
        self._count += 1  # Увеличиваем количество элементов

    def __len__(self):
        """
        Возвращает количество элементов в списке.
        """
        return self._count

    def __str__(self):
        """
        Преобразует список в строку.
        """
        if not len(self):  # Если список пустой
            return "None"
        else:
            a = self.head  # Начинаем с головы списка
            result = f"({a.value}) -> "  # Добавляем значение первого элемента
            while a.next:  # Проходим по списку
                a = a.next
                result += f"({a.value}) -> "  # Добавляем значения остальных элементов
            a = a.next  # Переходим к последнему элементу (None)
            result += f"{a}"  # Добавляем "None" в конец строки
            return result

    def __repr__(self):
        """
        Представление списка для отладки.
        """
        return str(self)  # Используем то же представление, что и для __str__

    def __eq__(self, n2):
        """
        Сравнивает два списка на равенство.
        """
        if isinstance(n2, MyList):  # Проверяем, является ли n2 списком MyList
            return str(self) == str(n2)  # Сравниваем строковые представления списков
        else:
            return False

    def __ne__(self, n2):
        """
        Сравнивает два списка на неравенство.
        """
        return not self == n2

    def __contains__(self, value):
        """
        Проверяет, содержится ли значение в списке.
        """
        if not len(self):  # Если список пустой
            return False
        else:
            a = self.head
            if a.value == value:  # Проверяем значение первого элемента
                return True
            while a.next:  # Проходим по списку
                a = a.next
                if a.value == value:  # Проверяем значения остальных элементов
                    return True
        return False 
    
    def remove(self, value):
        """
        Удаляет первое вхождение значения из списка.
        """
        if self.head is None:  # Если список пустой
            raise ValueError()
        if self.head.value == value:  # Если значение находится в голове списка
            self.head = self.head.next  # Удаляем голову
            self._count -= 1 
            return 
        current = self.head 
        while current.next:  # Проходим по списку
            if current.next.value == value:  # Если значение найдено
                current.next = current.next.next  # Удаляем узел
                self._count -= 1 
                return 
            current = current.next 
        raise ValueError()  # Если значение не найдено

    
    def pop(self):
        """
        Удаляет и возвращает последний элемент списка.
        """
        if self.head is None:  # Если список пустой
            raise IndexError('pop from empty list')
        current = self.head
        if current.next is None:  # Если в списке только один элемент
            value = current.value
            self.head = None  # Список становится пустым
            self._count -= 1 
            return value
        while current.next.next:  # Проходим по списку до предпоследнего элемента
            current = current.next
        value = current.next.value  # Сохраняем значение последнего элемента
        current.next = None  # Удаляем последний элемент
        self._count -= 1 
        return value

    def clear(self):
        """
        Очищает список.
        """
        self.head = None
        self._count = 0

    def extend(self, other):
        """
        Расширяет список, добавляя элементы из другого списка.
        """
        if isinstance(other, MyList) and other.head is not None:  # Проверяем, является ли other списком MyList
            a = other.head
            self.append(a.value)  # Добавляем элементы из other в конец текущего списка
            while a.next:
                a = a.next
                self.append(a.value)
        elif not isinstance(other, MyList): 
            raise TypeError()  # Выбрасываем исключение, если other не список MyList 

    def copy(self):
        """
        Создает копию списка.
        """
        new_list = MyList()
        current = self.head
        while current:  # Проходим по списку и добавляем элементы в новый список
            new_list.append(current.value)
            current = current.next
        return new_list

    def insert(self, index, value):
        """
        Вставляет элемент в список по указанному индексу.
        """
        if (not isinstance(index, int)) or index < 0:  # Проверяем корректность индекса
            raise IndexError() 
        if index >= self._count:  # Если индекс больше или равен длине списка, добавляем элемент в конец
            self.append(value)
            return
        if index == 0:  # Если индекс равен 0, вставляем элемент в начало списка
            new_node = ListNode(value, self.head)
            self.head = new_node
            self._count += 1 
            return
        current = self.head
        for _ in range(index - 1):  # Проходим по списку до нужного индекса
            current = current.next
            if current is None: 
                return
        new_node = ListNode(value, current.next)  # Создаем новый узел и вставляем его 
        current.next = new_node
        self._count += 1 

    def index(self, value):
        """
        Возвращает индекс первого вхождения значения в списке.
        """
        current = self.head
        idx = 0
        while current:  # Проходим по списку
            if current.value == value: 
                return idx 
            current = current.next
            idx += 1 
        raise ValueError(f"{value} is not in list")  # Если значение не найдено 

    def count(self, value):
        """
        Возвращает количество вхождений значения в списке.
        """
        _count = 0
        current = self.head
        while current:  # Проходим по списку
            if current.value == value: 
                _count += 1 
            current = current.next
        return _count 

    def reverse(self):
        """
        Развернуть список.
        """ 
        prev = None
        current = self.head 
        while current:  # Проходим по списку и меняем направление связей
            next_node = current.next
            current.next = prev
            prev = current 
            current = next_node 
        self.head = prev 