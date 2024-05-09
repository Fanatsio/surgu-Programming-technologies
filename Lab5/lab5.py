from collections import Counter
from heapq import heapify, heappop, heappush
from bitarray import bitarray

def compress(filename):
    """
    Compresses a PPM image using Vitter's algorithm.

    Args:
        filename: The path to the PPM image file.
    """

    with open(filename, 'rb') as f:
        # Read and ignore comment lines
        while True:
            line = f.readline().decode('utf-8').strip()  # Assuming UTF-8 encoding, adjust if needed
            if not line.startswith('#'):
                header = line.strip().split()
                break

        # Read width, height, and max value
        width, height = int(header[1]), int(header[2])
        max_val = int(f.readline().decode('utf-8').strip())

        # Read pixel data
        data = f.read()

    # Build symbol frequencies
    frequencies = Counter(data)

    # Create Huffman tree
    heap = [[weight, [symbol, ""]] for symbol, weight in frequencies.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Create codebook
    codebook = {symbol: code for weight, [symbol, code] in heap[0][1:]}

    # Encode data
    encoded_data = bitarray()
    for byte in data:
        encoded_data.extend(codebook[byte])

    # Write compressed data to file
    with open(f"{filename}.compressed", 'wb') as f:
        f.write(f"P6\n{width} {height}\n{max_val}\n".encode('utf-8'))
        f.write(encoded_data.tobytes())


def decompress(filename):
    """
    Decompresses a PPM image compressed using Vitter's algorithm.

    Args:
        filename: The path to the compressed PPM image file.
    """

    with open(filename, 'rb') as f:
        # Read PPM header
        header = f.readline().decode('utf-8').strip().split()
        width, height = int(header[1]), int(header[2])
        max_val = int(header[3])

        # Read encoded data
        encoded_data = bitarray()
        encoded_data.fromfile(f)

    # Build Huffman tree
    heap = [[weight, [symbol, ""]] for symbol, weight in Counter(encoded_data.tobytes()).items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    # Decode data
    decoded_data = bytearray()
    current_code = ""
    for bit in encoded_data:
        current_code += str(bit)
        for weight, [symbol, code] in heap[0][1:]:
            if code == current_code:
                decoded_data.append(symbol)
                current_code = ""
                break

    # Write decompressed data to file
    with open(f"{filename}.decompressed", 'wb') as f:
        f.write(f"P6\n{width} {height}\n{max_val}\n".encode('utf-8'))
        f.write(decoded_data)


def compare_files(original_file, decompressed_file):
    """
    Compares the original and decompressed files to check if they are identical.

    Args:
        original_file: The path to the original PPM image file.
        decompressed_file: The path to the decompressed PPM image file.

    Returns:
        True if the files are identical, False otherwise.
    """
    with open(original_file, 'rb') as f1, open(decompressed_file, 'rb') as f2:
        return f1.read() == f2.read()


# Example usage
filename = "input.ppm"  # Replace with your PPM file name
compress(filename)
decompress(f"{filename}.compressed")

if compare_files(filename, f"{filename}.decompressed"):
    print("Files are identical!")
else:
    print("Files are different!")