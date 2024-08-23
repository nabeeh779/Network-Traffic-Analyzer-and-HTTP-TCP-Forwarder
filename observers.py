"""Observer Interface"""
import logging
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