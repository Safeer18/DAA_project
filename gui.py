import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import pickle
import socket
import os

from huffman_utils import *

# --- File Paths ---
COMPRESSED_FILE = "compressed.bin"
RECEIVED_FILE = "received.bin"
DECOMPRESSED_FILE = "decompressed.txt"


def compress_and_save(filepath):
    with open(filepath, 'r') as file:
        data = file.read()

    freq = get_frequency(data)
    tree = build_huffman_tree(freq)
    codes = generate_codes(tree)
    encoded = encode_data(data, codes)
    padded = pad_encoded_data(encoded)
    byte_data = get_byte_array(padded)

    with open(COMPRESSED_FILE, 'wb') as file:
        pickle.dump((byte_data, tree), file)


def decompress_received_file():
    with open(RECEIVED_FILE, 'rb') as file:
        byte_data, tree = pickle.load(file)

    bit_string = ''.join(f"{byte:08b}" for byte in byte_data)
    extra_padding = int(bit_string[:8], 2)
    actual_data = bit_string[8:-extra_padding]
    decoded_text = decode_bit_string(actual_data, tree)

    with open(DECOMPRESSED_FILE, 'w') as file:
        file.write(decoded_text)

    return decoded_text


def send_file():
    try:
        s = socket.socket()
        s.bind(('localhost', 9999))
        s.listen(1)
        conn, addr = s.accept()

        with open(COMPRESSED_FILE, 'rb') as file:
            conn.sendall(file.read())

        conn.close()
        messagebox.showinfo("Success", "File sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Sender Error: {e}")


def receive_file():
    try:
        s = socket.socket()
        s.connect(('localhost', 9999))

        with open(RECEIVED_FILE, 'wb') as file:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                file.write(data)

        s.close()
        messagebox.showinfo("Success", "File received successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Receiver Error: {e}")


# ---------- GUI ----------
def start_gui():
    def browse_file():
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            file_label.config(text=filepath)
            selected_file[0] = filepath

    def compress_send():
        if not selected_file[0]:
            messagebox.showwarning("Warning", "No file selected!")
            return
        compress_and_save(selected_file[0])
        threading.Thread(target=send_file).start()

    def receive_decompress():
        threading.Thread(target=receive_file).start()
        # Delay decompression to let file fully receive
        root.after(2000, show_decompressed)

    def show_decompressed():
        if os.path.exists(RECEIVED_FILE):
            text = decompress_received_file()
            output_window.delete("1.0", tk.END)
            output_window.insert(tk.END, text)
        else:
            messagebox.showerror("Error", "No file received yet.")

    root = tk.Tk()
    root.title("Huffman File Transfer GUI")
    root.geometry("600x400")

    selected_file = [None]

    tk.Label(root, text="Huffman File Transfer", font=("Helvetica", 16, "bold")).pack(pady=10)

    tk.Button(root, text="📁 Browse File", command=browse_file).pack()
    file_label = tk.Label(root, text="No file selected", fg="gray")
    file_label.pack()

    tk.Button(root, text="📦 Compress & Send", bg="#cde", command=compress_send).pack(pady=10)
    tk.Button(root, text="📥 Receive & Decompress", bg="#cfc", command=receive_decompress).pack()

    output_window = tk.Text(root, height=10, wrap=tk.WORD)
    output_window.pack(pady=10)

    root.mainloop()


if __name__ == '__main__':
    start_gui()
