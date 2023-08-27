import numpy as np
from math import cos, sin, pi
from struct import pack, unpack

from src.Constants import Constants


class Reconstructor3D():

    def create_point_cloud(self, scan_path: str):
        # data_front = self.process_binary_file(f"{scan_path}{Constants.SENSOR_IP_FRONT}.bin")
        # data_right = self.process_binary_file(f"{scan_path}{Constants.SENSOR_IP_RIGHT}.bin")
        # data_left = self.process_binary_file(f"{scan_path}{Constants.SENSOR_IP_LEFT}.bin")
        data_top = self.process_binary_file(f"{scan_path}{'192.168.10.28'}.bin")

        xyz = np.array([[xy[0], xy[1], 0] for xy in data_top])

        with open(f"{scan_path}data.npy", "wb") as file:
            np.save(file, xyz)

    def process_binary_file(self, file_path: str):
        file = open(file_path, "rb")
        data = file.read()
        file.close()

        xy = list()
        magic_byte = pack("H", 0xa25c)

        for packet in data.split(magic_byte):

            if len(packet) <= 10:
                continue

            # packet_type = unpack("H", packet[:2])[0]
            packet_size = unpack("I", packet[2:6])[0] - len(magic_byte)
            header_size = unpack("H", packet[6:8])[0] - len(magic_byte)
            # scan_number = unpack("H", packet[8:10])[0]
            # packet_number = unpack("H", packet[10:12])[0]
            # timestamp_raw = ...
            # timestamp_sync = ...
            # status_flags = unpack("I", packet[28:32])[0]
            # scan_frequency = unpack("I", packet[32:36])[0]
            # num_points_scan = unpack("H", packet[36:38])[0]
            # num_points_packet = unpack("H", packet[38:40])[0]
            # first_index = unpack("H", packet[40:42])[0]
            first_angle = unpack("i", packet[42:46])[0]
            angular_increment = unpack("i", packet[46:50])[0]

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
            # print(f"first_angle: {first_angle}")
            # print(f"angular_increment: {angular_increment}")
            # print("---------------------------------------")

            if len(packet) != packet_size:
                print("corrupted package...")
                continue

            payload = packet[header_size:]  # list[uint32] - 4byte
            distances = unpack(f"{len(payload) // 4}I", payload[:len(payload) // 4 * 4])

            xy.extend(self.polar_to_xy(distances, first_angle, angular_increment))

        return xy

    def polar_to_xy(self, distances: list, first_angle: int, angular_increment: int) -> list[tuple[float, float]]:
        first_angle /= 10000
        angular_increment /= 10000

        xy = list()

        for i, distance in enumerate(distances):
            angle = (first_angle + i * angular_increment) * pi / 180.0

            x = round(distance * cos(angle))
            y = round(distance * sin(angle))

            xy.append((x, y))

        return xy