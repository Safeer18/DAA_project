import os
from huffman_utils import *

RECEIVED_FILE = "received.bin"
DECOMPRESSED_OUTPUT_FOLDER = "received_files"

def decompress_received_file():
    os.makedirs(DECOMPRESSED_OUTPUT_FOLDER, exist_ok=True)

    with open(RECEIVED_FILE, 'rb') as file:
        header = file.read(4)

        if header == b'HUFF':
            tree_len_bytes = file.read(4)
            tree_length = int.from_bytes(tree_len_bytes, 'big')
            tree_data = file.read(tree_length)
            tree_bits = ''.join(f"{byte:08b}" for byte in tree_data)
            tree_bits_unpadded = tree_bits[8:]
            tree = deserialize_tree(tree_bits_unpadded)

            compressed_data = file.read()
            bit_string = ''.join(f"{byte:08b}" for byte in compressed_data)
            extra_padding = int(bit_string[:8], 2)
            actual_data = bit_string[8:-extra_padding]

            decoded_text = decode_bit_string(actual_data, tree)
            output_path = os.path.join(DECOMPRESSED_OUTPUT_FOLDER, "decompressed.txt")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(decoded_text)

            print(f"[Decompressor] ✅ Huffman decompressed to {output_path}")
            return output_path

        elif header == b'RAWF':
            name_line = b''
            while True:
                byte = file.read(1)
                if byte == b'\n':
                    break
                name_line += byte
            filename = name_line.decode('utf-8')
            data = file.read()

            output_path = os.path.join(DECOMPRESSED_OUTPUT_FOLDER, filename)
            with open(output_path, 'wb') as f:
                f.write(data)

            print(f"[Decompressor] ✅ Raw file written to {output_path}")
            return output_path

        else:
            print("[Decompressor] ❌ Unknown file header")
            return None
