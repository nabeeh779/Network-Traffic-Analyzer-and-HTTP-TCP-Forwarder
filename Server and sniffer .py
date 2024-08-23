import os
import scapy.all as scapy
import logging
import socket
import threading
import multiprocessing
from ProtocolHandle import *
logging.basicConfig(filename='network_analyzer.log', level=logging.INFO)  # setting up log file


def tcp_server():
    """This Function Run Tcp server on host 0.0.0.0 means all interfaces and port 8888"""
    def handle_client(client_socket, forward_to_host, forward_to_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as forward_socket:
            forward_socket.connect((forward_to_host, forward_to_port))
            request = client_socket.recv(4096)  # Reading data from given request
            forward_socket.send(request)  # Sending data as forward
            response = forward_socket.recv(4096)  # Reading response
            client_socket.send(response)  # Froward response to client (We are working as proxy)
        client_socket.close()  # Close Client socket

    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_STREAM)  # Init stream socket , AF_INENT - Internet Protocol , SOCK_STREAM - We want a stream-based protocol because of TCP.
    sock.bind(("0.0.0.0", 8888))  # Bind to all interfaces on port 8888
    sock.listen(5)  # Listen mode with a backlog of 5
    logging.info("TCP Forwarder listening on port 8888")
    while True:
        client_socket, addr = sock.accept()  # (host, port)
        logging.info(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(
        client_socket, "example.com", 80))  # Using thread, we call handle_client function.
        client_thread.start()

"""Initialize protocol handlers"""
protocol_handlers = [
    DnsHandler(),     # For DNS traffic
    HttpHandler(),    # For HTTP traffic
    FTPHandler(),     # For FTP traffic
    SMTPHandler(),    # For SMTP traffic
    EthHandler() # For Ethernet frames
]
def packet_sniffer():
    """This function sniff packets in the network and checks if the packet contains tcp/http layer"""
    def packet_callback(packet1):
        for handler in protocol_handlers:   #  Iterate through protocol handlers.
            if handler.detect(packet1):    #  If handler can process the packet
                handler.process_packet(packet1) #  Process the packet
    packet = scapy.sniff(store=False,
                         iface="Intel(R) Wi-Fi 6 AX201 160MHz", prn=packet_callback)  # choose the network interface


def main():
    # Establishing sniffer and tcpServer processes.
    sniffer_process = multiprocessing.Process(target=packet_sniffer)
    tcp_server_process = multiprocessing.Process(target=tcp_server)
    # Starting processes
    sniffer_process.start()
    tcp_server_process.start()
    # Wait for processes to complete
    sniffer_process.join()
    tcp_server_process.join()


if __name__ == "__main__":
    main()
    print("lol")
