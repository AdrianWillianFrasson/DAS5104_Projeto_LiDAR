import numpy as np
import open3d as o3d
from math import cos, sin, pi
from struct import pack, unpack

from src.Constants import Constants


class Reconstructor3D():

    def create_point_cloud(self, scan_path: str):
        # scans_front = self.process_binary_file(f"{scan_path}{Constants.SENSOR_FRONT_IP}.bin")
        scans_right = self.process_binary_file(f"{scan_path}{Constants.SENSOR_RIGHT_IP}.bin")
        scans_left = self.process_binary_file(f"{scan_path}{Constants.SENSOR_LEFT_IP}.bin")
        scans_top = self.process_binary_file(f"{scan_path}{Constants.SENSOR_TOP_IP}.bin")
        # ---------------------------------------------------------------------
        xyz = list()

        # speed = self.calculate_speed(scans_front)
        speed = []

        xyz_right = self.reconstruct_z_axis(scans_right, speed)
        xyz_left = self.reconstruct_z_axis(scans_left, speed)
        xyz_top = self.reconstruct_z_axis(scans_top, speed)

        xyz_right = self.transform(xyz_right, Constants.SENSOR_RIGHT_ROTATION, Constants.SENSOR_RIGHT_TRANSLATION)
        xyz_left = self.transform(xyz_left, Constants.SENSOR_LEFT_ROTATION, Constants.SENSOR_LEFT_TRANSLATION)

        xyz.extend(xyz_right)
        xyz.extend(xyz_left)
        xyz.extend(xyz_top)
    
    
        xyz = self.remove_xy(xyz, Constants.BOUNDING_BOX_X_MIN,Constants.BOUNDING_BOX_X_MAX, Constants.BOUNDING_BOX_Y_MIN, Constants.BOUNDING_BOX_Y_MAX)
        # Remove paredes.
        # if (x <= 0) or (y <= -1000) or (y >= 1000):
        # continue

        # ---------------------------------------------------------------------
        np.savez_compressed(f"{scan_path}data.npz", xyz=xyz)

    def process_binary_file(self, file_path: str) -> dict:
        file = open(file_path, "rb")
        data = file.read()
        file.close()

        scans = dict()
        magic_byte = pack("H", 0xa25c)

        for packet in data.split(magic_byte):

            if len(packet) <= 10:
                continue

            try:
                # packet_type = unpack("H", packet[:2])[0]
                packet_size = unpack("I", packet[2:6])[0] - len(magic_byte)
                header_size = unpack("H", packet[6:8])[0] - len(magic_byte)
                scan_number = unpack("H", packet[8:10])[0]
                # packet_number = unpack("H", packet[10:12])[0]
                timestamp_raw = unpack("Q", packet[12:20])[0]
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
                # print(f"timestamp_raw: {timestamp_raw}")
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

            if scan_number not in scans:
                scans[scan_number] = dict()
                scans[scan_number]["xy"] = list()
                scans[scan_number]["timestamp_raw"] = self.ntp64_to_seconds(timestamp_raw)

            payload = packet[header_size:]  # list[uint32] - 4byte
            distances = unpack(f"{len(payload) // 4}I", payload[:len(payload) // 4 * 4])

            scans[scan_number]["xy"].extend(self.polar_to_xy(distances, first_angle, angular_increment))

        return scans

    def ntp64_to_seconds(self, integer) -> float:
        # Upper 32 bits for seconds
        seconds = integer >> 32

        # Lower 32 bits for fractional seconds
        fractional_seconds = integer & 0xFFFFFFFF
        fractional_seconds = fractional_seconds / 0x100000000

        return round(seconds + fractional_seconds, 3)

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

    def calculate_speed(self, scans_front: dict) -> dict:
        pass

    def reconstruct_z_axis(self, scans: dict, speed: dict) -> list[tuple[int, int, int]]:
        xyz = list()

        scan_keys = list(scans.keys())
        scan_keys.sort()

        for i, scan_key in enumerate(scan_keys):

            for xy in scans[scan_key]["xy"]:
                x = xy[0]
                y = xy[1]
                z = i * 2

                xyz.append((x, y, z))

        return xyz

    def transform(self, points, rotation, translation):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        rotation_matrix = pcd.get_rotation_matrix_from_xyz(rotation)

        pcd.translate(translation)
        pcd.rotate(rotation_matrix, center=(0, 0, 0))

        return np.asarray(pcd.points)

    def remove_xy(self, points, x_min,x_max,y_min,y_max):
        list_xyz = []
        for i in range(len(points)):
            if points[i][0] <= x_min or points[i][1] <= x_max or points[i][1] >= y_min or points[i][0] >= y_max:
                continue
            list_xyz.append(points[i])
        return list_xyz

    