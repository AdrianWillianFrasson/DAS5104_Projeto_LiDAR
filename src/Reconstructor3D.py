import numpy as np
import open3d as o3d
from math import cos, sin, pi
from struct import pack, unpack

from src.Constants import Constants


class Reconstructor3D():

    def create_point_cloud(self, scan_path: str):
        scans_front = self.process_binary_file(f"{scan_path}{Constants.SENSOR_FRONT_IP}.bin")
        # scans_right = self.process_binary_file(f"{scan_path}{Constants.SENSOR_RIGHT_IP}.bin")
        # scans_left = self.process_binary_file(f"{scan_path}{Constants.SENSOR_LEFT_IP}.bin")
        scans_top = self.process_binary_file(f"{scan_path}{Constants.SENSOR_TOP_IP}.bin")

        # ---------------------------------------------------------------------
        xyz = list()

        z_axis, xyz_front = self.calculate_z_axis(
            scans_front,
            Constants.BOUNDARIES_ZAXIS_X_MIN,
            Constants.BOUNDARIES_ZAXIS_X_MAX,
            Constants.BOUNDARIES_ZAXIS_Y_MIN,
            Constants.BOUNDARIES_ZAXIS_Y_MAX,
        )

        # xyz_right = self.reconstruct_z_axis(scans_right, z_axis)
        # xyz_left = self.reconstruct_z_axis(scans_left, z_axis)
        xyz_top = self.reconstruct_z_axis(scans_top, z_axis)

        # xyz_right = self.transform(xyz_right, Constants.SENSOR_RIGHT_ROTATION, Constants.SENSOR_RIGHT_TRANSLATION)
        # xyz_left = self.transform(xyz_left, Constants.SENSOR_LEFT_ROTATION, Constants.SENSOR_LEFT_TRANSLATION)

        # xyz_right = self.remove_boundaries(
        #     xyz_right,
        #     Constants.BOUNDARIES_PROFILE_X_MIN,
        #     Constants.BOUNDARIES_PROFILE_X_MAX,
        #     Constants.BOUNDARIES_PROFILE_Y_MIN,
        #     Constants.BOUNDARIES_PROFILE_Y_MAX,
        # )

        # xyz_left = self.remove_boundaries(
        #     xyz_left,
        #     Constants.BOUNDARIES_PROFILE_X_MIN,
        #     Constants.BOUNDARIES_PROFILE_X_MAX,
        #     Constants.BOUNDARIES_PROFILE_Y_MIN,
        #     Constants.BOUNDARIES_PROFILE_Y_MAX,
        # )

        xyz_top = self.remove_boundaries(
            xyz_top,
            Constants.BOUNDARIES_PROFILE_X_MIN,
            Constants.BOUNDARIES_PROFILE_X_MAX,
            Constants.BOUNDARIES_PROFILE_Y_MIN,
            Constants.BOUNDARIES_PROFILE_Y_MAX,
        )

        # xyz_top = self.remove_boundaries_3D(
        #     xyz_top,
        #     Constants.BOUNDARIES_PROFILE_X_MIN,
        #     Constants.BOUNDARIES_PROFILE_X_MAX,
        #     -420,
        #     0,
        #     -2400,
        #     -1750,
        # )

        # xyz_right = self.filter_point_cloud(xyz_right, 15, 40, 0.1, 25, 50)
        # xyz_left = self.filter_point_cloud(xyz_left, 15, 40, 0.1, 25, 50)
        # xyz_top = self.filter_point_cloud(xyz_top, 8, 80, 0.2, 130, 120)
        xyz_top = self.filter_point_cloud(xyz_top, 15, 60, 0.06, 25, 120)

        # xyz.extend(xyz_front)  # Debug
        # xyz.extend(xyz_right)
        # xyz.extend(xyz_left)
        xyz.extend(xyz_top)

        xyz = self.transform(xyz, (0, 0, -pi/2), (0, Constants.SENSOR_TOP_HEIGHT, 0))

        # ---------------------------------------------------------------------
        return xyz

    def process_binary_file(self, file_path: str):
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

    def ntp64_to_seconds(self, integer):
        # Upper 32 bits for seconds
        seconds = integer >> 32

        # Lower 32 bits for fractional seconds
        fractional_seconds = integer & 0xFFFFFFFF
        fractional_seconds = fractional_seconds / 0x100000000

        return round(seconds + fractional_seconds, 3)

    def polar_to_xy(self, distances: list, first_angle: int, angular_increment: int):
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

    def calculate_z_axis(self, scans_front: dict, x_min: int, x_max: int, y_min: int, y_max: int):
        z_axis = {}
        xyz_front = []

        for i, scan_key in enumerate(sorted(scans_front.keys())):
            # z_axis[i] = z_axis.get(i-1, y_min)
            z_axis[i] = y_min

            for xy in scans_front[scan_key]["xy"]:
                x = xy[0]
                y = xy[1]
                z = i * 5

                if x <= x_min or x >= x_max or y <= y_min or y >= y_max:
                    continue

                if y > z_axis[i]:
                    z_axis[i] = y

                xyz_front.append((x, y, z))

        return z_axis, xyz_front

    def reconstruct_z_axis(self, scans: dict, z_axis: dict) -> list[tuple[int, int, int]]:
        xyz = list()

        for key in zip(sorted(scans.keys()), sorted(z_axis.keys())):

            for xy in scans[key[0]]["xy"]:
                x = xy[0]
                y = xy[1]
                z = z_axis[key[1]]

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

    def remove_boundaries(self, points, x_min: int, x_max: int, y_min: int, y_max: int):
        return [p for p in points if not (p[0] <= x_min or p[0] >= x_max or p[1] <= y_min or p[1] >= y_max)]

    def remove_boundaries_3D(self, points, x_min, x_max, y_min, y_max, z_min, z_max):
        return [p for p in points if not (p[0] <= x_min or p[0] >= x_max or p[1] <= y_min or p[1] >= y_max or p[2] <= z_min or p[2] >= z_max)]

    def filter_point_cloud(self, points, voxel_size, nb_neighbors, std_ratio, nb_points, radius):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        xyz_1 = pcd.voxel_down_sample(voxel_size=voxel_size)
        xyz_2, _ = xyz_1.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)
        xyz_3, _ = xyz_2.remove_radius_outlier(nb_points=nb_points, radius=radius)

        return np.asarray(xyz_3.points)
