"""Observer Interface"""
import logging
import scapy.all as scapy
logging.basicConfig(
    filename='network_analyzer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

#  Observer classes
class PacketObserver:
    def update(self, packet):
        raise NotImplementedError

class LoggingObserver(PacketObserver):
    def update(self, packet):
        logging.info(f"Packet logged: {packet.summary()}") # Log packet summary to file

class AnalysisObserver(PacketObserver):
    def update(self, packet):
        print(f"Analyzing packet: {packet.summary()}")

class CaptureObserver(PacketObserver):
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file

    def update(self, packet):
        try:
            scapy.wrpcap(self.pcap_file, [packet], append=True)
            logging.info(f"Packet captured and saved to {self.pcap_file}")
        except Exception as e:
            logging.error(f"Error capturing packet: {e}")

class AnalyzeObserver(PacketObserver):
    def __init__(self, pcap_file):
        self.pcap_file = pcap_file

    def update(self, packet):
        print(f"Analyzing packet: {packet.summary()}")

    def analyze(self):
        try:
            packets = scapy.rdpcap(self.pcap_file)
            for packet in packets:
                print(packet.summary())  # Example analysis
        except Exception as e:
            logging.error(f"Error during packet analysis: {e}")