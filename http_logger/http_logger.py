from socket import *
import sys
import loggers

server_address = "0.0.0.0"
port = 8080
logger = loggers.logger_maker()


def socket_error_handler(exception):
    loggers.logger_save(logger, f"{exception}", 0)
    sys.exit(1)


def http_response(method):
    """ This function Prepare HTTP response """
    if method == "GET":
        response_body = "GET request received"
    elif method == "POST":
        response_body = "POST request received"
    else:
        response_body = "Unsupported HTTP method"
    response = (
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: text/plain\r\n"
        f"Content-Length: {len(response_body)}\r\n"
        "\r\n"
        f"{response_body}"
    )
    return response


def handle_client_connection(client_socket):
    """This Function Handle Client connection"""
    try:
        request = client_socket.recv(1024).decode("utf-8")
        if request:
            print(f"Received data:\n{request}\n")
        else:
            print("No data received. Connection might be closed.")
    except Exception as e:
        print(f"Socket error: {e}")
        socket_error_handler(client_socket)

    loggers.logger_save(logger, f"Received request: {request}", 1)
    # Parse HTTP request line and headers
    lines = request.splitlines()
    request_line = lines[0]  # Taking first line
    method, path, _ = request_line.split(" ")
    headers = {}
    for line in lines[1:]:  # Skip first line
        if line == "":
            break  # End
        else:
            key, value = line.split(": ", 1)  # Get Key and value
            headers[key] = value
    # Log method, path, and headers
    loggers.logger_save(
        logger, f"Method: {method}, Path: {path}, Headers: {headers}", 1
    )

    # Sending response
    try:
        client_socket.sendall(http_response(method).encode("utf-8"))
        # Optionally, receive a response to verify data was processed
        response = client_socket.recv(4096)
        print("Response received:")
        print(response.decode("utf-8"))
    except socket.error as e:
        print(f"Socket error: {e}")
        socket_error_handler(e)
    client_socket.close()


def server():
    """This is a tcp server"""
    try:
        server_socket = socket(AF_INET, SOCK_STREAM, 0)
    except Exception as e:
        print("Creating socket failed\n ")
        socket_error_handler(e)
    try:
        server_socket.bind((server_address, port))
    except Exception as e:
        print("Socket Binding failed\n ")
        socket_error_handler(e)
    try:
        server_socket.listen(5)
    except Exception as e:
        print("Socket listen failed\n ")
        socket_error_handler(e)

    print(f"Starting TCP HTTP server on port {port}...")
    while 1:
        try:
            client_socket, _ = server_socket.accept()
        except Exception as e:
            print("server socket accept failed\n ")
            socket_error_handler(e)
        handle_client_connection(client_socket)


def main():
    server()


if __name__ == "__main__":
    main()
