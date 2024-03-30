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

def mixed_array_sort(arr):
    root = None
    for item in arr:
        node = Node(item)
        if root is None:
            root = node
        else:
            insert(root, node)
    sorted_arr = inorder_traversal(root)
    return sorted_arr

# Пример использования:
# mixed_array = ["banana", "apple", "grape", "orange", "kiwi", "pineapple"]
# mixed_array = ["apple", "3", "banana", "grape", "1", "orange"]
with open('sort_benchmark.txt', 'r') as file:
        mixed_array = []
        for line in file:
            mixed_array.append(line.strip())
sorted_array = mixed_array_sort(mixed_array)
print("Sorted array:", sorted_array)
