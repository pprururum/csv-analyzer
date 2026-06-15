"""
Модуль с реализацией односвязного списка

Используется для демонстрации загрузки данных в связный список
на первом этапе конвейера обработки
"""

class Node:
    """Узел односвязного списка"""
    def __init__(self, value):
        """Инициализация узла"""
        self.value = value
        self.next = None


class LinkedList:
    """Односвязный список для хранения числовых данных"""
    def __init__(self):
        """Инициализация пустого списка"""
        self.head = None
        self._length = 0

    def append(self, value):
        """Добавление элемента в конец списка"""
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._length = self._length + 1

    def to_list(self):
        """Преобразование связного списка в обычный Python-список"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self):
        """Возвращает количество элементов в списке"""
        return self._length

    def __iter__(self):
        """Итератор по элементам списка"""
        current = self.head
        while current is not None:
            yield current.value
            current = current.next

    def __repr__(self):
        """Строковое представление списка"""
        values = []
        for v in self:
            values.append(str(v))
        return "LinkedList([" + ", ".join(values) + "])"