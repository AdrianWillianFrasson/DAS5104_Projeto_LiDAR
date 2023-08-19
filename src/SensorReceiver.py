# import struct
# import numpy as np
from socketserver import UDPServer, DatagramRequestHandler
from threading import Thread


class SensorReceiver(Thread):

    def __init__(self, server_ip: str, server_port: int):
        super().__init__(daemon=True)

        self.server_ip = server_ip
        self.server_port = server_port

        self.server_udp = UDPServer((server_ip, server_port), self.UDPHandler)

    def stop(self):
        self.server_udp.shutdown()

    def run(self):
        self.server_udp.serve_forever()

    class UDPHandler(DatagramRequestHandler):

        def handle(self):
            print(f"{SensorReceiver.lul} {self.client_address}: {self.rfile.read()}")
