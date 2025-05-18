import socket

def send_file():
    s = socket.socket()
    s.bind(('localhost', 9999))
    s.listen(1)
    print("Sender: Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected to {addr}")

    with open("compressed.bin", 'rb') as file:
        data = file.read()
        conn.sendall(data)

    print("File sent successfully.")
    conn.close()

if __name__ == '__main__':
    send_file()
