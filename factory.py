"""Factory Pattern"""

from ProtocolHandle import *  #  ProtocolHandle.py contains protocols handlers functions.


class ProtocolHandlerFactory:
    @staticmethod
    #  Create handlers by protocol type
    def create_handler(protocol_type):
        if protocol_type == "HTTP":
            return HttpHandler()
        if protocol_type == "DNS":
            return DnsHandler()
        if protocol_type == "Ether":
            return EthHandler()
        if protocol_type == "FTP":
            return FTPHandler()
        if protocol_type == "SMTP":
            return SMTPHandler()
        else:
            raise ValueError(f"Unhandled protocol type: {protocol_type}")
