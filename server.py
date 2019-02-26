import socket
from threading import Thread


def server_start():
    print("Starting Server")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('',7614))

    while True:
        msg, address = server_socket.recvfrom(1024)
        print(msg)


if __name__ == "__main__":

    server = Thread(target=
                    server_start, args=[])
    server.start()
