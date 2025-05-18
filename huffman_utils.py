import heapq

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def get_frequency(data):
    freq = {}
    for char in data:
        freq[char] = freq.get(char, 0) + 1
    return freq

def build_huffman_tree(freq_dict):
    heap = [Node(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def generate_codes(node, code='', huffman_codes={}):
    if node is None:
        return

    if node.char is not None:
        huffman_codes[node.char] = code

    generate_codes(node.left, code + '0', huffman_codes)
    generate_codes(node.right, code + '1', huffman_codes)

    return huffman_codes

def encode_data(data, huffman_codes):
    return ''.join(huffman_codes[char] for char in data)

def pad_encoded_data(encoded_data):
    extra_padding = 8 - len(encoded_data) % 8
    encoded_data += '0' * extra_padding
    padded_info = "{0:08b}".format(extra_padding)
    return padded_info + encoded_data

def get_byte_array(padded_data):
    byte_array = bytearray()
    for i in range(0, len(padded_data), 8):
        byte_array.append(int(padded_data[i:i+8], 2))
    return byte_array

def decode_bit_string(bit_string, huffman_tree):
    decoded_text = ""
    current_node = huffman_tree

    for bit in bit_string:
        current_node = current_node.left if bit == '0' else current_node.right
        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = huffman_tree

    return decoded_text
