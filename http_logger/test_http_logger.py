import socket
import pytest
import subprocess
import time
import http_logger

SERVER_PORT = 8080


# Helper function to start the server
def start_server():
    server_process = subprocess.Popen(['python', 'http_logger.py'])  # Start tcp_http_logger script
    time.sleep(1)  # Wait to start
    return server_process


# Helper function to stop the server
def stop_server(server_process):
    server_process.terminate()
    server_process.wait()


# Helper function to send an HTTP request and get the response
def send_request(method, path, body=''):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_sock:
        client_sock.connect(('localHost', SERVER_PORT))
        request = f"{method} {path} HTTP/1.1\r\nHost: localhost\r\nContent-Length: {len(body)}\r\n\r\n{body}"
        client_sock.sendall(request.encode('utf-8'))
        response = client_sock.recv(4096).decode('utf-8')
    return response


# Test unsupported http methods
def test_unsupported_http_methods():
    server_process = start_server()
    try:
        response = send_request('PUT', '/test')
        assert "Unsupported HTTP method" in response
        assert "HTTP/1.1 200 OK" in response
    finally:
        stop_server(server_process)


def test_get_request():
    """Test GET request handling"""
    server_process = start_server()
    response = send_request('GET', '/test')
    assert "GET request received" in response
    assert "HTTP/1.1 200 OK" in response


def test_post_request():
    """Test POST request handling"""
    server_process = start_server()
    response = send_request('POST', '/test', 'key=value')
    assert "POST request received" in response
    assert "HTTP/1.1 200 OK" in response
