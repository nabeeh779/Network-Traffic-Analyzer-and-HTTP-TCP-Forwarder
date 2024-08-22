import os
import scapy.all as scapy
import logging
import socket
import threading
import multiprocessing
logging.basicConfig(filename='network_analyzer.log', level=logging.INFO)  # setting up log file


def tcp_server():
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


def packet_sniffer():
    """This function sniff packets in the network and checks if the packet contains tcp/http layer"""

    def packet_callback(packet1):

        print("packet: " + str(packet1))
        # if packet1.haslayer(scapy.TCP) and packet1.haslayer(scapy.Raw):  # Check if packet contains TCP layer
        if packet1.haslayer(scapy.Raw):
            data = packet1[scapy.Raw].load  # Load the raw data.
            if b"HTTP" in data:  # Detection of http
                # store src ip and dst ip
                print("HTTP traffic detected!")
                src_ip = packet1[scapy.IP].src
                dst_ip = packet1[scapy.IP].dst
                logging.info(f"HTTP Packet: {src_ip} -> {dst_ip}, Payload: {data[:50]}")  # saving into file

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
