import pickle
from huffman_utils import *

def decompress_file(input_path, output_path):
    with open(input_path, 'rb') as file:
        byte_data, huffman_tree = pickle.load(file)

    bit_string = ''.join(f"{byte:08b}" for byte in byte_data)
    padding_info = bit_string[:8]
    extra_padding = int(padding_info, 2)
    actual_bit_string = bit_string[8:-extra_padding]

    decoded_text = decode_bit_string(actual_bit_string, huffman_tree)

    with open(output_path, 'w') as file:
        file.write(decoded_text)

    print(f"File decompressed and saved to {output_path}")

if __name__ == '__main__':
    decompress_file("received.bin", "decompressed.txt")
