import pytest

from list_node import ListNode
from my_list import MyList
from test_data import *

@pytest.mark.listnode
def test_single_node_init():
    value = 10
    node = ListNode(value)
    assert node.value == value
    assert node.next == node  # В кольцевом списке должен ссылаться сам на себя
    assert node.prev == node  # Аналогично, ссылка назад на себя

@pytest.mark.listnode
def test_double_node_init():
    value1 = 10
    value2 = 20
    node1 = ListNode(value1)
    node2 = ListNode(value2, node1, node1)
    node1.next = node2
    node1.prev = node2
    assert node1.next == node2
    assert node1.prev == node2
    assert node2.next == node1
    assert node2.prev == node1

@pytest.mark.listnode
def test_node_str():
    value = 10
    node = ListNode(value)
    assert str(node) == f"({value})"

@pytest.mark.listnode
def test_node_eq():
    node1 = ListNode(10)
    node2 = ListNode(10, node1, node1)
    node1.prev = node2
    node1.next = node2
    assert node1 == node2

@pytest.mark.mylist
def test_list_init_empty():
    lst = MyList()
    assert lst.head is None
    assert lst.tail is None
    assert len(lst) == 0

@pytest.mark.mylist
def test_list_init_nonempty():
    values = [10, 20, 30]
    lst = MyList(*values)
    assert len(lst) == len(values)
    assert lst.head.value == values[0]
    assert lst.tail.value == values[-1]
    assert lst.head.prev == lst.tail
    assert lst.tail.next == lst.head

@pytest.mark.mylist
def test_list_append():
    lst = MyList()
    values = [10, 20, 30]
    for value in values:
        lst.append(value)
        assert lst.tail.value == value
        assert lst.tail.next == lst.head
        assert lst.head.prev == lst.tail

@pytest.mark.mylist
def test_list_remove():
    lst = MyList(10, 20, 30)
    lst.remove(20)
    assert len(lst) == 2
    assert lst.head.next == lst.tail
    assert lst.tail.prev == lst.head
    with pytest.raises(ValueError):
        lst.remove(100)  # Попытка удалить несуществующий элемент

@pytest.mark.mylist
def test_list_reverse():
    lst = MyList(10, 20, 30)
    lst.reverse()
    assert lst.head.value == 30
    assert lst.head.next.value == 20
    assert lst.tail.value == 10
    assert lst.tail.prev.value == 20

@pytest.mark.mylist
def test_list_copy():
    lst1 = MyList(10, 20, 30)
    lst2 = lst1.copy()
    assert lst1 != lst2
    assert len(lst1) == len(lst2)
    assert lst1.head.value == lst2.head.value
    assert lst1.tail.value == lst2.tail.value

@pytest.mark.mylist
def test_list_extend():
    lst1 = MyList(10, 20)
    lst2 = MyList(30, 40)
    lst1.extend(lst2)
    assert len(lst1) == 4
    assert lst1.tail.value == 40
    assert lst1.head.next.next.value == 30

@pytest.mark.mylist
def test_list_pop():
    lst = MyList(10, 20, 30)
    value = lst.pop()
    assert value == 30
    assert len(lst) == 2
    assert lst.tail.value == 20
    with pytest.raises(IndexError):
        MyList().pop()  # Попытка вытащить элемент из пустого списка

@pytest.mark.mylist
def test_list_index():
    lst = MyList(10, 20, 30, 40)
    index = lst.index(30)
    assert index == 2
    with pytest.raises(ValueError):
        lst.index(100)  # Несуществующий элемент

@pytest.mark.mylist
def test_list_count():
    lst = MyList(10, 20, 10, 10, 30)
    assert lst.count(10) == 3
    assert lst.count(20) == 1
@pytest.mark.mylist
def test_list_sort():
    lst = MyList(30, 10, 20, 40, 50)
    lst.sort()
    sorted_values = [10, 20, 30, 40, 50]
    current = lst.head
    for value in sorted_values:
        assert current.value == value
        current = current.next

@pytest.mark.mylist
def test_list_sort_empty():
    lst = MyList()
    lst.sort()
    assert lst.head is None
    assert lst.tail is None
    assert len(lst) == 0

@pytest.mark.mylist
def test_list_sort_single_element():
    lst = MyList(10)
    lst.sort()
    assert lst.head.value == 10
    assert lst.tail.value == 10
    assert len(lst) == 1

@pytest.mark.mylist
def test_linear_search():
    lst = MyList(10, 20, 30, 40, 50)
    node = lst.linear_search(30)
    assert node is not None
    assert node.value == 30
    node = lst.linear_search(60)
    assert node is None

@pytest.mark.mylist
def test_linear_search_empty():
    lst = MyList()
    node = lst.linear_search(10)
    assert node is None

@pytest.mark.mylist
def test_linear_search_first_element():
    lst = MyList(10, 20, 30)
    node = lst.linear_search(10)
    assert node is not None
    assert node.value == 10

@pytest.mark.mylist
def test_linear_search_last_element():
    lst = MyList(10, 20, 30)
    node = lst.linear_search(30)
    assert node is not None
    assert node.value == 30

@pytest.mark.mylist
def test_binary_search():
    lst = MyList(10, 20, 30, 40, 50)
    index = lst.binary_search(30)
    assert index == 2
    index = lst.binary_search(60)
    assert index == -1

@pytest.mark.mylist
def test_binary_search_empty():
    lst = MyList()
    index = lst.binary_search(10)
    assert index == -1

@pytest.mark.mylist
def test_binary_search_first_element():
    lst = MyList(10, 20, 30)
    index = lst.binary_search(10)
    assert index == 0

@pytest.mark.mylist
def test_binary_search_last_element():
    lst = MyList(10, 20, 30)
    index = lst.binary_search(30)
    assert index == 2

if __name__ == "__main__":
    pytest.main()
