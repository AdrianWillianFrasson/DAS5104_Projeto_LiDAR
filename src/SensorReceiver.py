from socketserver import UDPServer, DatagramRequestHandler
from threading import Thread
from struct import unpack
# import numpy as np


class SensorReceiver(Thread):

    distances = []

    def __init__(self, server_ip: str, server_port: int):
        super().__init__(daemon=True)

        self.server_ip = server_ip
        self.server_port = server_port

        self.server_udp = UDPServer((server_ip, server_port), self.Handler)

    def stop(self):
        self.server_udp.shutdown()

    def run(self):
        self.server_udp.serve_forever()

    class Handler(DatagramRequestHandler):

        def handle(self):
            address = self.client_address[0]
            data = self.rfile.read()

            if len(data) <= 2:
                print("Staring...")
                return

            # magic = unpack("H", data[:2])[0]
            # packet_type = unpack("H", data[2:4])[0]
            packet_size = unpack("I", data[4:8])[0]
            header_size = unpack("H", data[8:10])[0]
            # scan_number = unpack("H", data[10:12])[0]
            # packet_number = unpack("H", data[12:14])[0]
            # timestamp_raw = ...
            # timestamp_sync = ...
            # status_flags = unpack("I", data[30:34])[0]
            # scan_frequency = unpack("I", data[34:38])[0]
            # num_points_scan = unpack("H", data[38:40])[0]
            # num_points_packet = unpack("H", data[40:42])[0]
            # first_index = unpack("H", data[42:44])[0]
            first_angle = unpack("i", data[44:48])[0]
            # angular_increment = unpack("i", data[48:52])[0]

            # print(f"magic: {hex(magic)}")
            # print(f"packet_type: {hex(packet_type)}")
            # print(f"packet_size: {packet_size}")
            # print(f"header_size: {header_size}")
            # print(f"scan_number: {scan_number}")
            # print(f"packet_number: {packet_number}")
            # print(f"status_flags: {status_flags}")
            # print(f"scan_frequency: {scan_frequency}")
            # print(f"num_points_scan: {num_points_scan}")
            # print(f"num_points_packet: {num_points_packet}")
            # print(f"first_index: {first_index}")
            print(f"first_angle: {first_angle}")
            # print(f"angular_increment: {angular_increment}")
            print("---------------------------------------")

            if len(data) != packet_size:
                print("corrupted package...")
                return

            payload = data[header_size:]  # list[uint32] - 4byte
            distances = unpack(f"{len(payload) // 4}I", payload[:len(payload) // 4 * 4])
            print(f"distances ({len(distances)}): {distances}")
