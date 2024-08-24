from scapy.all import IP, Raw, DNS, Ether, TCP  # type: ignore

"""Protocol Handler"""


class ProtocolHandler:
    """Base of all protocol handlers"""

    def __init__(self):
        self.src_ip = None
        self.dst_ip = None

    def extract_ip(self, packet):
        #  This function detects if packet contains src ip and dst ip
        if packet.haslayer(IP):
            self.src_ip = packet[IP]
            self.dst_ip = packet[IP]

    def detect(self, packet):
        """Detect if the packet matches the protocol. To be overridden by subclasses."""
        raise NotImplementedError

    def process_packet(self, packet):
        """Process the packet if it matches the protocol. To be overridden by subclasses."""
        raise NotImplementedError


class HttpHandler(ProtocolHandler):
    """HTTP Protocol handle"""

    def detect(self, packet):
        #  Check if packet contains http.
        return packet.haslayer(scapy.all.Raw) and b"HTTP" in packet[scapy.all.Raw].load

    def process_packet(self, packet):
        #  Process the HTTP Packet.
        self.extract_ip(packet)  #  Extract ip from packets
        if self.src_ip and self.dst_ip:
            print(
                f"HTTP Packet detected: {self.src_ip} -> {self.dst_ip}, Payload: {packet[scapy.all.Raw].load[:50]}"
            )


class DnsHandler(ProtocolHandler):
    """
    DNS protocol Handler.
    DNS stands for - Domain Name Server.
    """

    def detect(self, packet):
        #  Check if packet contains dns layer.
        return packet.haslayer(DNS)

    def process_packet(self, packet):
        # Process The DNS packet.
        self.extract_ip(packet)  #  Extarct ip
        if self.src_ip and self.dst_ip:
            query = packet[DNS].qd.qname
            print(
                f"DNS Packet detected: {self.src_ip} -> {self.dst_ip}, Query: {query}"
            )


class EthHandler(ProtocolHandler):
    """Ethernet Protocol handler"""

    def __int__(self):
        super().__init__()
        self.dst_mac = none
        self.src_mac = none

    def extract_mac(self, packet):
        """Extract source and destination MAC addresses from the Ethernet frame"""
        if packet.haslayer(Ether):
            self.src_mac = packet[Ether].src
            self.dst_mac = packet[Ether].dst

    def detect(self, packet):
        #  Check if contains eth frame
        return packet.haslayer(Ether)

    def process_packet(self, packet):
        """Process the Ethernet frame"""
        self.extract_mac(packet)  #  Getting mac address
        if self.src_mac and self.dst_mac:
            print(f"Ethernet Frame detected: {self.src_mac} -> {self.dst_mac}")


class FTPHandler(ProtocolHandler):
    """
    Handles detection and processing of FTP packets.
    FTP traffic, operates over TCP on port 21.
    FTP stands for - File Transfer Protocol
    """

    def detect(self, packet):
        # Check if the packet contains FTP traffic.
        # Port 21 used for control connection.
        # Port 20 used for Data connection.
        return packet.haslayer(TCP) and (
            packet[TCP].dport == 21 or packet[TCP].dport == 20
        )

    def process_packet(self, packet):
        self.extract_ip(packet)
        print(f"FTP Packet detected: {src_ip} -> {dst_ip}")
        # If the packet has a TCP payload, get ftp commands.
        if packet.haslayer(TCP) and packet[TCP].payload:
            ftp_data = str(packet[TCP].payload)
            print(f"FTP Data: {ftp_data}")


class SMTPHandler(ProtocolHandler):
    """
    Handles detection and processing of SMTP packets
    SMTP stands for - Simple Mail Transfer Protocol
    """

    def detect(self, packet):
        #  Detect if the packet contains SMTP traffic.
        #  Check if the packet contains a TCP layer and if the destination or source port is 25, 465, or 587 (SMTP).
        #  port 25 for unencrypted email ,  ports 465/587 for encrypted email (using SSL/TLS).
        return packet.haslayer(TCP) and (
            packet[TCP].dport in [25, 465, 587] or packet[TCP].sport in [25, 465, 587]
        )

    def process_packet(self, packet):
        self.extract_ip(packet)
        if self.src_ip and self.dst_ip:
            print(f"SMTP Packet detected: {self.src_ip} -> {self.dst_ip}")
            # If the packet has a TCP payload, print the SMTP commands (optional)
            if packet.haslayer(TCP) and packet[TCP].payload:
                smtp_data = str(packet[TCP].payload)
                print(f"SMTP Data: {smtp_data}")
