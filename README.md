# Network-Traffic-Analyzer-and-HTTP-TCP-Forwarder

## Overview

Network-Traffic-Analyzer-and-HTTP-TCP-Forwarder is a Python-based tool designed to capture and analyze network traffic. It utilizes the `scapy` library to capture TCP packets and a custom implementation to forward HTTP requests over TCP. The application leverages threading and multiprocessing to efficiently handle multiple concurrent connections.

## Features

- **Network Traffic Analysis**: Capture and analyze TCP packets using `scapy`.
- - **Protocol handlers** for DNS, HTTP, FTP, SMTP, and Ethernet .
- **HTTP Forwarding**: Forward HTTP requests over TCP using socket programming.
- **Concurrency**: Handle multiple connections simultaneously using threading and multiprocessing.

