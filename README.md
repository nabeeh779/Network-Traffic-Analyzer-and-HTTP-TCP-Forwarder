# Network-Traffic-Analyzer-and-HTTP-TCP-Forwarder

## Overview

Network-Traffic-Analyzer-and-HTTP-TCP-Forwarder is a Python tool designed to capture and analyze network traffic. Utilizing the `scapy` library for TCP packet analysis, it also forwards HTTP requests over TCP. The application leverages threading and multiprocessing for efficient handling of multiple concurrent connections.

## Features

- **Network Traffic Analysis**: Capture and analyze TCP packets using `scapy`.
- **Protocol Handlers**: Support for DNS, HTTP, FTP, SMTP, and Ethernet protocols.
- **HTTP Forwarding**: Forward HTTP requests over TCP using socket programming.
- **Concurrency**: Handle multiple connections simultaneously with threading and multiprocessing.

## Design Patterns

- **Strategy Pattern**: Modularizes protocol handling by defining a common interface for protocol handlers and using them dynamically based on packet type.
- **Factory Pattern**: Manages the instantiation of protocol handlers through a factory class, simplifying code and management.
- **Observer Pattern**: Implements a notification system to alert components about packet detection events, enabling flexible and scalable event handling.

## Requirements

- Python 3.x
- `scapy` library

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nabeeh779/Network-Traffic-Analyzer-and-HTTP-TCP-Forwarder.git

