import pickle
from huffman_utils import *

def compress_file(input_path, output_path):
    with open(input_path, 'r') as file:
        data = file.read()

    freq = get_frequency(data)
    huffman_tree = build_huffman_tree(freq)
    codes = generate_codes(huffman_tree)
    encoded_data = encode_data(data, codes)
    padded_data = pad_encoded_data(encoded_data)
    byte_data = get_byte_array(padded_data)

    with open(output_path, 'wb') as output:
        pickle.dump((byte_data, huffman_tree), output)

    print(f"File compressed and saved to {output_path}")

if __name__ == '__main__':
    compress_file("test.txt", "compressed.bin")
