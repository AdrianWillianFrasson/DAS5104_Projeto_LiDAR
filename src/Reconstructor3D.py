import numpy as np
from math import cos, sin, pi
from struct import pack, unpack

from src.Constants import Constants


class Reconstructor3D():

    def create_point_cloud(self, scan_path: str):
        # xy_front = self.process_binary_file(f"{scan_path}{Constants.SENSOR_IP_FRONT}.bin")
        # xy_right = self.process_binary_file(f"{scan_path}{Constants.SENSOR_IP_RIGHT}.bin")
        # xy_left = self.process_binary_file(f"{scan_path}{Constants.SENSOR_IP_LEFT}.bin")
        xy_top = self.process_binary_file(f"{scan_path}{Constants.SENSOR_IP_TOP}.bin")
        # ---------------------------------------------------------------------

        xyz = list()
        count = 0

        for i, xy in enumerate(xy_top):
            x = xy[0]
            y = xy[1]
            z = count * 1

            # Avança na profundidade (Z-axe).
            if (i % 332) == 0:
                count += 1

            # Remove paredes.
            # if (x <= 0) or (y <= -1000) or (y >= 1000):
                # continue

            xyz.append([x, y, z])

        # ---------------------------------------------------------------------
        np.savez_compressed(f"{scan_path}data.npz", xyz=xyz)

    def process_binary_file(self, file_path: str) -> list[tuple[int, int]]:
        file = open(file_path, "rb")
        data = file.read()
        file.close()

        xy = list()
        magic_byte = pack("H", 0xa25c)

        for packet in data.split(magic_byte):

            if len(packet) <= 10:
                continue

            try:
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
            except Exception:
                print("[Exception] corrupted package...")
                continue

            if len(packet) != packet_size:
                print("[packet_size] corrupted package...")
                continue

            payload = packet[header_size:]  # list[uint32] - 4byte
            distances = unpack(f"{len(payload) // 4}I", payload[:len(payload) // 4 * 4])

            xy.extend(self.polar_to_xy(distances, first_angle, angular_increment))

        return xy

    def polar_to_xy(self, distances: list, first_angle: int, angular_increment: int) -> list[tuple[int, int]]:
        first_angle /= 10000
        angular_increment /= 10000

        xy = list()

        for i, distance in enumerate(distances):
            # Invalid measurements return 0xFFFFFFFF
            if distance == 4_294_967_295:
                continue

            angle = (first_angle + i * angular_increment) * pi / 180.0

            x = round(distance * cos(angle))
            y = round(distance * sin(angle))

            xy.append((x, y))

        return xy
