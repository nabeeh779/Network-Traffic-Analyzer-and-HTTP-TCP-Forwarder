import os
import scapy.all as scapy
import logging
import socket
import threading
import multiprocessing
from ProtocolHandle import *
from packet_sniffer import *
from observers import *
from factory import *

# setting up logging
logging.basicConfig(
    filename='network_analyzer.log',
    level=logging.INFO ,
    format='%(asctime)s - %(levelname)s - %(message)s')


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

"""Initialize protocols """
protocols = ["HTTP", "DNS", "FTP", "SMTP", "Ether"]
def packet_sniffer():
    """This function sniff packets in the network"""
    try:
        #  Initialize register observers
        logging_observer = LoggingObserver()
        analysis_observer = AnalysisObserver()
        #  Initialize PacketSniffer
        sniffer = PacketSniffer()
        sniffer.register_observer(logging_observer)
        sniffer.register_observer(analysis_observer)

        #  Add protocols handlers
        for p in protocols:
            try:
                handler = ProtocolHandlerFactory.create_handler(p)
                sniffer.protocol_handlers.append(handler)
            except Exception as e:
                logging.error(f"Error creating handler for protocol {p}: {e}")

        #  Start sniffing by calling scapy.sniff and direct packets to sniffer.sniff_packets function
        try:
            scapy.sniff(store=False,
                                 iface="Intel(R) Wi-Fi 6 AX201 160MHz", prn=sniffer.sniff_packets)  # iface - network interface
        except Exception as e:
                logging.error(f"Error packet sniffing: {e}")
    except Exception as e:
        logging.error(f"Error initializing packet sniffer Function: {e}")
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
