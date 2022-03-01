import socket
import locale
import time

locale.setlocale(locale.LC_ALL, 'en_US')

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
max_length = 65500
f = open("gb.txt", "rb")

messages_number = 0
bytes_number = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    start_time = time.time()
    block = f.read(max_length)
    while block:
        s.sendall(block)
        messages_number += 1
        bytes_number += len(block)
        block = f.read(max_length)
    print("Client TCP")
    print(f'Sent {messages_number}: {locale.format("%d", bytes_number, grouping=True)}')
    print("--- %s seconds ---" % (time.time() - start_time))


f.close()
