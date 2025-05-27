import socket

def receive_file():
    s = socket.socket()
    s.connect(('localhost', 9999))

    with open("received.bin", 'wb') as file:
        while True:
            data = s.recv(1024)
            if not data:
                break
            file.write(data)

    print("File received and saved as received.bin")
    s.close()

if __name__ == '__main__':
    receive_file()
