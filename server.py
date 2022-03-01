import socket
import locale

locale.setlocale(locale.LC_ALL, 'en_US')

HOST = "127.0.0.1"
PORT = 65432
max_length = 65500

serverType = 1

while serverType != 0:
    serverType = int(input("Select a option:\n 1 for TCP\n 2 for UDP\n 3 for UDP stop and wait \n "))

    f = open("result.txt", "wb")
    f.write(b'')
    f.close()
    f = open("result.txt", "ab")
    messages_number = 0
    bytes_number = 0

    if serverType == 1:  # TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen()
            conn, addr = sock.accept()
            with conn:
                print(f"Connected by {addr}")
                data = conn.recv(max_length)
                while data:
                    messages_number += 1
                    # if len(data) != max_length:
                    #     print(f"Received {messages_number}: {len(data)}")
                    bytes_number += len(data)
                    f.write(data)
                    data = conn.recv(max_length)
        print(f'Server TCP execution done')

    elif serverType == 2:  # UDP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, PORT))
            data, addr = sock.recvfrom(max_length)
            sock.settimeout(3)
            print(f"Connected by {addr}")
            while data:
                try:
                    messages_number += 1
                    # print(f"Received {messages_number}: {len(data)}")
                    bytes_number += len(data)
                    f.write(data)
                    data, addr = sock.recvfrom(max_length)
                except socket.timeout:
                    print("socket.timeout: closing socket")
                    break
        print(f'Server UDP stream execution done')

    elif serverType == 3:  # UDP stop and wait
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((HOST, PORT))
            while True:
                try:
                    data, addr = sock.recvfrom(max_length)
                    sock.sendto(b'1', addr)
                    messages_number += 1
                    bytes_number += len(data)
                    f.write(data)
                    sock.settimeout(3)
                except socket.timeout:
                    print("socket.timeout: closing socket")
                    break
        print(f'Server UDP stop and wait execution done')

    print(f'Received {messages_number}: {locale.format("%d", bytes_number, grouping=True)} \n')
    f.close()
