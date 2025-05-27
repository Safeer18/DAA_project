import heapq
from collections import defaultdict


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def get_frequency(data):
    freq = defaultdict(int)
    for char in data:
        freq[char] += 1
    return freq

def build_huffman_tree(freq):
    heap = [Node(char, f) for char, f in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = Node(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)

    return heap[0] if heap else None

def generate_codes(node, current="", codes=None):
    if codes is None:
        codes = {}
    if node is not None:
        if node.char is not None:
            codes[node.char] = current
        generate_codes(node.left, current + "0", codes)
        generate_codes(node.right, current + "1", codes)
    return codes

def encode_data(data, codes):
    return ''.join(codes[char] for char in data)

def pad_encoded_data(data):
    extra_padding = 8 - len(data) % 8
    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + data + "0" * extra_padding

def get_byte_array(padded_data):
    byte_array = bytearray()
    for i in range(0, len(padded_data), 8):
        byte_array.append(int(padded_data[i:i+8], 2))
    return byte_array

def decode_bit_string(bit_string, tree):
    result = ""
    current = tree
    for bit in bit_string:
        current = current.left if bit == '0' else current.right
        if current.char is not None:
            result += current.char
            current = tree
    return result

def serialize_tree(node):
    if node is None:
        return '0'
    if node.char is not None:
        return '1' + format(ord(node.char), '08b')
    return '2' + serialize_tree(node.left) + serialize_tree(node.right)

def deserialize_tree(bits, index=0):
    def _deserialize(i):
        if bits[i] == '0':
            return None, i + 1
        if bits[i] == '1':
            char = chr(int(bits[i+1:i+9], 2))
            return Node(char, 0), i + 9
        if bits[i] == '2':
            left, i = _deserialize(i + 1)
            right, j = _deserialize(i)
            node = Node(None, 0)
            node.left = left
            node.right = right
            return node, j
    return _deserialize(index)[0]

