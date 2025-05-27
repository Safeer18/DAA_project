import os
from huffman_utils import *

COMPRESSED_FILE = "compressed.bin"
COMPRESSIBLE_EXTENSIONS = ('.txt', '.json', '.csv', '.log', '.xml')

def compress_and_save(filepath):
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filepath)[1].lower()

    is_compressible = ext in COMPRESSIBLE_EXTENSIONS
    with open(filepath, 'rb') as file:
        data = file.read()

    if is_compressible:
        try:
            text = data.decode('utf-8')
            freq = get_frequency(text)
            tree = build_huffman_tree(freq)
            codes = generate_codes(tree)
            encoded = encode_data(text, codes)
            padded = pad_encoded_data(encoded)
            byte_data = get_byte_array(padded)

            tree_bits = serialize_tree(tree)
            padded_tree = pad_encoded_data(tree_bits)
            tree_bytes = get_byte_array(padded_tree)

            with open(COMPRESSED_FILE, 'wb') as f:
                f.write(b'HUFF')
                f.write(len(tree_bytes).to_bytes(4, 'big'))
                f.write(tree_bytes)
                f.write(byte_data)

            print(f"[Compressor] ✅ Huffman compressed '{filename}'")
            return
        except Exception as e:
            print(f"[Compressor] ❌ Failed to compress '{filename}': {e}")
            is_compressible = False

    if not is_compressible:
        with open(COMPRESSED_FILE, 'wb') as f:
            f.write(b'RAWF')
            f.write(filename.encode('utf-8') + b'\n')
            f.write(data)
        print(f"[Compressor] 🔁 Sent raw file '{filename}' without compression")
