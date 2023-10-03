import numpy as np
import open3d as o3d
from math import cos, sin, pi
from struct import pack, unpack

from src.Constants import Constants


class Reconstructor3D():

    def create_point_cloud(self, scan_path: str):
        scans_front = self.process_binary_file(f"{scan_path}{Constants.SENSOR_FRONT_IP}.bin")
        scans_right = self.process_binary_file(f"{scan_path}{Constants.SENSOR_RIGHT_IP}.bin")
        scans_left = self.process_binary_file(f"{scan_path}{Constants.SENSOR_LEFT_IP}.bin")
        scans_top = self.process_binary_file(f"{scan_path}{Constants.SENSOR_TOP_IP}.bin")

        # ---------------------------------------------------------------------
        xyz = list()

        speeds, xyz_front = self.calculate_speeds2(
            scans_front,
            Constants.BOUNDING_BOX_SPEED_X_MIN,
            Constants.BOUNDING_BOX_SPEED_X_MAX,
            Constants.BOUNDING_BOX_SPEED_Y_MIN,
            Constants.BOUNDING_BOX_SPEED_Y_MAX,
        )

        xyz_right = self.reconstruct_z_axis2(scans_right, speeds)
        xyz_left = self.reconstruct_z_axis2(scans_left, speeds)
        xyz_top = self.reconstruct_z_axis2(scans_top, speeds)

        xyz_right = self.transform(xyz_right, Constants.SENSOR_RIGHT_ROTATION, Constants.SENSOR_RIGHT_TRANSLATION)
        xyz_left = self.transform(xyz_left, Constants.SENSOR_LEFT_ROTATION, Constants.SENSOR_LEFT_TRANSLATION)

        # xyz.extend(xyz_front)
        xyz.extend(xyz_right)
        xyz.extend(xyz_left)
        xyz.extend(xyz_top)

        xyz = self.remove_xy(
            xyz,
            Constants.BOUNDING_BOX_PROFILE_X_MIN,
            Constants.BOUNDING_BOX_PROFILE_X_MAX,
            Constants.BOUNDING_BOX_PROFILE_Y_MIN,
            Constants.BOUNDING_BOX_PROFILE_Y_MAX,
        )

        xyz = self.filter_point_cloud(xyz)

        # ---------------------------------------------------------------------
        np.savez_compressed(f"{scan_path}data.npz", xyz=xyz)

    def process_data(self, scan_path: str, sensor: str):
        match sensor:
            case "top":
                return self.process_binary_file(f"{scan_path}{Constants.SENSOR_TOP_IP}.bin")
            case "left":
                return self.process_binary_file(f"{scan_path}{Constants.SENSOR_LEFT_IP}.bin")
            case "right":
                return self.process_binary_file(f"{scan_path}{Constants.SENSOR_RIGHT_IP}.bin")
            case "front":
                return self.process_binary_file(f"{scan_path}{Constants.SENSOR_FRONT_IP}.bin")
            case _:
                raise Exception("Invalid sensor")

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
                scans[scan_number]["timestamp"] = self.ntp64_to_seconds(timestamp_raw)

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

    def calculate_speeds(self, scans_front: dict, x_min: int, x_max: int, y_min: int, y_max: int) -> list:
        biggest_y = {}
        xyz_front = []
        speeds = []

        for i, scan_key in enumerate(sorted(scans_front.keys())):
            biggest_y[i] = {}
            biggest_y[i]["y"] = biggest_y.get(i-1, {"y": y_min})["y"]
            biggest_y[i]["timestamp"] = scans_front[scan_key]["timestamp"]

            for xy in scans_front[scan_key]["xy"]:
                x = xy[0]
                y = xy[1]
                z = i * 5

                if x <= x_min or x >= x_max or y <= y_min or y >= y_max:
                    continue

                if y > biggest_y[i]["y"]:
                    biggest_y[i]["y"] = y

                xyz_front.append((x, y, z))

        sorted_keys = sorted(biggest_y.keys())

        for i in range(len(sorted_keys) - 1):
            y_curr = biggest_y[sorted_keys[i]]
            y_next = biggest_y[sorted_keys[i+1]]

            speed = (y_next["y"] - y_curr["y"]) / (y_next["timestamp"] - y_curr["timestamp"])

            if speed < 0.0:
                speed = 0.0

            speeds.append(round(speed))

        return speeds, xyz_front

    def calculate_speeds2(self, scans_front: dict, x_min: int, x_max: int, y_min: int, y_max: int) -> dict:
        biggest_y = {}
        xyz_front = []

        for i, scan_key in enumerate(sorted(scans_front.keys())):
            # biggest_y[i] = biggest_y.get(i-1, y_min)
            biggest_y[i] = y_min

            for xy in scans_front[scan_key]["xy"]:
                x = xy[0]
                y = xy[1]
                z = i * 5

                if x <= x_min or x >= x_max or y <= y_min or y >= y_max:
                    continue

                if y > biggest_y[i]:
                    biggest_y[i] = y

                xyz_front.append((x, y, z))

        return biggest_y, xyz_front

    def reconstruct_z_axis(self, scans: dict, speeds: list) -> list[tuple[int, int, int]]:
        xyz = list()

        sorted_keys = sorted(scans.keys())
        z = 0

        for i in range(len(speeds) - 1):

            for xy in scans[sorted_keys[i]]["xy"]:
                x = xy[0]
                y = xy[1]

                xyz.append((x, y, z))

            dt = scans[sorted_keys[i+1]]["timestamp"] - scans[sorted_keys[i]]["timestamp"]
            z += round(speeds[i] * dt)

        return xyz

    def reconstruct_z_axis2(self, scans: dict, speeds: dict) -> list[tuple[int, int, int]]:
        xyz = list()

        for key in zip(sorted(scans.keys()), sorted(speeds.keys())):

            for xy in scans[key[0]]["xy"]:
                x = xy[0]
                y = xy[1]
                z = speeds[key[1]]

                xyz.append((x, y, z))

        return xyz

    def transform(self, points, rotation: tuple[int, int, int], translation: tuple[int, int, int]):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        if rotation != (0, 0, 0):
            rotation_matrix = pcd.get_rotation_matrix_from_xyz(rotation)
            pcd.rotate(rotation_matrix, center=(0, 0, 0))

        if translation != (0, 0, 0):
            pcd.translate(translation)

        return np.asarray(pcd.points)

    def remove_xy(self, points, x_min: int, x_max: int, y_min: int, y_max: int):
        return [p for p in points if not (p[0] <= x_min or p[0] >= x_max or p[1] <= y_min or p[1] >= y_max)]

    def filter_point_cloud(self, points):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        xyz_1, _ = pcd.remove_radius_outlier(nb_points=10, radius=60)
        xyz_2, _ = xyz_1.remove_statistical_outlier(nb_neighbors=60, std_ratio=0.7)

        return np.asarray(xyz_2.points)
