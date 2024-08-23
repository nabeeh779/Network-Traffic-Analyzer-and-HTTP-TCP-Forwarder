
"""Packet Sniffer class is the subject in the observer pattern"""
class PacketSniffer:
    def __init__(self):
        self.observers = []  #  List to save observers
        self.protocol_handlers = []  #  List to save protocolHandlers

    def register_observer(self, observer):
        #  This function append new observer to observers list
        self.observers.append(observer)

    def unregister_observer(self, observer):
        #  This function delete observer from observers list
        self.observers.remove(observer)

    def notify_observers(self, packet):
        #  This function notify observers
        for observer in self.observers:
            observer.update(packet)

    def sniff_packets(self, packet):
        # This function calls process_packet of all current packets
        for handler in self.protocol_handlers:
            if handler.detect(packet):
                handler.process_packet(packet)
        # Notify observers
        self.notify_observers(packet)
