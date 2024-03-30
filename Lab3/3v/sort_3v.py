def menu():
    print("1 - Сортировка вставками\n"
          "2 - Сортировка бинарным деревом\n"
          "0 - Выход")
    return int(input("Введите >> "))


def is_sorted(array):
    return all(array[i] <= array[i + 1] for i in range(len(array) - 1))


def insertion_sort(array):
    for i in range(len(array)):
        key = array[i]
        j = i - 1
        while j >= 0 and str(array[j]) > str(key):
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key
    return array


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(root, node):
    if root is None:
        root = node
    else:
        if root.value < node.value:
            if root.right is None:
                root.right = node
            else:
                insert(root.right, node)
        else:
            if root.left is None:
                root.left = node
            else:
                insert(root.left, node)

def inorder_traversal(root):
    result = []
    if root:
        result += inorder_traversal(root.left)
        result.append(root.value)
        result += inorder_traversal(root.right)
    return result

def tree_sort(arr):
    root = None
    for item in arr:
        node = Node(item)
        if root is None:
            root = node
        else:
            insert(root, node)
    sorted_arr = inorder_traversal(root)
    return sorted_arr