import socket
import threading
import multiprocessing


def test_client():
    """This Function run client server and send data to tcp server to test it """
    def handle_client():
        server_address = (socket.gethostname(), 8888)  # Address of the proxy server
        message = b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(server_address)  # Connect to server address
            sock.sendall(message)  # Sending message we created.
            response = sock.recv(4096)  # Getting Server Response
            print(response.decode())  # Print server response


def main():
    client_process = multiprocessing.Process(target=test_client)
    client_process.start()
    client_process.join()


if __name__ == "__main__":
    main()
