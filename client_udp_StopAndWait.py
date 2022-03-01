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

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(3)
    block = f.read(max_length)
    start_time = time.time()
    while block:
        sock.sendto(block, (HOST, PORT))
        try:
            data, addr = sock.recvfrom(1)
        except socket.timeout:
            print("socket.timeout: resend")
        else:
            bytes_number += len(block)
            block = f.read(max_length)
        messages_number += 1
    print("Client UDP stop and wait")
    print(f'Sent {messages_number}: {locale.format("%d", bytes_number, grouping=True)}')
    print("--- %s seconds ---" % (time.time() - start_time))

f.close()

