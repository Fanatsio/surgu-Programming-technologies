class ListNode:
    def __init__(self, value=None, next=None, prev=None):
        self.value = value
        if next is None:
            # Если следующий узел не задан, узел ссылается сам на себя (для одиночного элемента)
            self.next = self
        else:
            self.next = next

        if prev is None:
            # Если предыдущий узел не задан, узел ссылается сам на себя (для одиночного элемента)
            self.prev = self
        else:
            self.prev = prev

        # Если узел не одиночный, настраиваем связи
        if self.next == self:
            self.next.prev = self
            self.prev.next = self

    def __str__(self):
        # Возвращаем только значение, чтобы избежать бесконечного вывода в кольцевом списке
        return f"({self.value})"

    def __eq__(self, other):
        if not isinstance(other, ListNode):
            return False
        # Сравниваем только значения, так как ссылки в кольцевом списке могут создать бесконечный цикл
        return self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    