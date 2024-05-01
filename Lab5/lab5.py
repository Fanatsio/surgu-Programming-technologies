import heapq
import hashlib

class Node:
    def __init__(self, symbol, freq):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    priority_queue = [Node(symbol, freq) for symbol, freq in freq_dict.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_codewords_table(node, code="", codewords_table={}):
    if node is not None:
        if node.symbol is not None:
            codewords_table[node.symbol] = code
        codewords_table = build_codewords_table(node.left, code + "0", codewords_table)
        codewords_table = build_codewords_table(node.right, code + "1", codewords_table)
    return codewords_table

def encode_symbol(symbol, codewords_table):
    return codewords_table[symbol]

def encode_text(text, codewords_table):
    encoded_text = ""
    for symbol in text:
        encoded_text += encode_symbol(symbol, codewords_table)
    return encoded_text

def compress(input_file, output_file):
    with open(input_file, 'rb') as f:
        content = f.read()

    freq_dict = {}
    for byte in content:
        freq_dict[byte] = freq_dict.get(byte, 0) + 1

    huffman_tree = build_huffman_tree(freq_dict)  # Сохраняем дерево Хаффмана
    codewords_table = build_codewords_table(huffman_tree)

    encoded_text = encode_text(content, codewords_table)

    # Write the encoded text to the output file
    with open(output_file, 'wb') as f:
        f.write(encoded_text.encode())

    return codewords_table, huffman_tree  # Возвращаем таблицу кодов и дерево Хаффмана

def decode_text(encoded_text, huffman_tree):
    decoded_text = ""
    current_node = huffman_tree
    for bit in encoded_text:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.symbol is not None:
            decoded_text += chr(current_node.symbol)
            current_node = huffman_tree
    return decoded_text

def decompress(input_file, output_file, codewords_table, huffman_tree):
    # Read the encoded text from the input file
    with open(input_file, 'rb') as f:
        encoded_text = f.read()

    # Decode the encoded text using the codewords table
    decoded_text = decode_text(encoded_text.decode(), huffman_tree)

    # Write the decoded text to the output file
    with open(output_file, 'wb') as f:
        f.write(decoded_text.encode())



def hash_file(file_path):
    """Generate a hash for a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def compare_files(file1, file2):
    """Compare two files by their hashes."""
    hash1 = hash_file(file1)
    hash2 = hash_file(file2)
    if hash1 == hash2:
        print("Файлы", file1, "и", file2, "идентичны.")
    else:
        print("Файлы", file1, "и", file2, "не идентичны.")

def main():
    input_file = "input.ppm"
    output_file = "compressed.ppm"

    # Compression
    codewords_table, huffman_tree = compress(input_file, output_file)  # Получаем таблицу кодов и дерево Хаффмана
    print("Compression successful.")

    # Decompression
    input_file_compressed = "compressed.ppm"
    output_file_decompressed = "decompressed.ppm"

    decompress(input_file_compressed, output_file_decompressed, codewords_table, huffman_tree)  # Передаем дерево Хаффмана
    print("Decompression successful.")

    # Compare files
    compare_files(input_file, output_file)

if __name__ == "__main__":
    main()
