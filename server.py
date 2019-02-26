import datetime
import socket
from threading import Thread

''' Default Connection Values '''
UDP_URL_BIND = '0.0.0.0'
UDP_PORT_BIND = 7000

TCP_URL_BIND = '0.0.0.0'
TCP_PORT_BIND = 7001

TCPClientSockets = [] # The TCP Sockets that will be populated by tcp_connect


def logging(msg):
    """
    Logs Data in the Console for Debugging
    :param msg: The message to be sent to the console for printing
    """
    current_dt = datetime.datetime.now()

    print("{} {}\n".format(current_dt.strftime("%H:%M:%S"), msg))


def udp_server():
    """
    Creates a UDP Server. To be run in a thread
    """

    logging("Initializing UDP Server")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Initialises the Server Socket
    server_socket.bind((UDP_URL_BIND, UDP_PORT_BIND))  # Binds the Socket to Specified URL and Port

    logging("Listening for UDP Data on port {}".format(UDP_PORT_BIND))

    while True:
        msg, address = server_socket.recvfrom(1024)
        logging("Received {} from {}:{}".format(msg, address[0], address[1]))

        serve_data = Thread(target=tcp_send, args=[msg])  # Creates a Thread to Send the Data received
        serve_data.start()  # Starts the thread to send the data along


def tcp_send(msg):
    """
    Sends data over TCP to the Sockets stored in the TCPClientSockets Array
    :param msg: The message to be sent over TCP
    """

    for client in TCPClientSockets:  # Loops through all the known TCP Connections and sends the data
        client.send(msg)

    logging("Sent \"{}\" to {} connected clients".format(msg, len(TCPClientSockets)))


def tcp_connect():
    """
    Accepts a TCP connection and stores it in the TCPClientSockets Array
    """

    logging("Initializing TCP Server")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Initialises the Server Socket
    server.bind((TCP_URL_BIND, TCP_PORT_BIND))  # Binds the Socket to Specified URL and Port

    logging("Listening for TCP Connections on port {}".format(TCP_PORT_BIND))

    server.listen(5)  # Start with max of 5 backlog connections

    while True:
        client_sock, address = server.accept()  # Accepts the Connection
        logging("Accepted Connection from {}:{}".format(address[0], address[1]))
        TCPClientSockets.append(client_sock)  # Adds the Socket to the list of known clients


if __name__ == "__main__":
    udp_thread = Thread(target=udp_server)  # The UDP Server
    tcp_send_thread = Thread(target=tcp_connect)  # The TCP Server

    # Start the Respective Servers
    udp_thread.start()
    tcp_send_thread.start()
