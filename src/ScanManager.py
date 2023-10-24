from subprocess import Popen

from src.Constants import Constants
from src.SensorManager import SensorManager


class ScanManager():

    def __init__(self):
        self.server_ip = Constants.SERVER_IP
        self.server_port = Constants.SERVER_PORT

        self.sensor_front = SensorManager(Constants.SENSOR_FRONT_IP, self.server_ip, self.server_port)
        self.sensor_right = SensorManager(Constants.SENSOR_RIGHT_IP, self.server_ip, self.server_port)
        self.sensor_left = SensorManager(Constants.SENSOR_LEFT_IP, self.server_ip, self.server_port)
        self.sensor_top = SensorManager(Constants.SENSOR_TOP_IP, self.server_ip, self.server_port)

        self.rust_exec = None

    def start_scan(self, output_folder: str):
        print(self.sensor_front.set_parameters(samples_per_scan=600,
              scan_frequency=50, scan_direction=Constants.SCAN_DIRECTION))
        print(self.sensor_right.set_parameters(samples_per_scan=600,
              scan_frequency=50, scan_direction=Constants.SCAN_DIRECTION))
        print(self.sensor_left.set_parameters(samples_per_scan=600,
              scan_frequency=50, scan_direction=Constants.SCAN_DIRECTION))
        print(self.sensor_top.set_parameters(samples_per_scan=600,
              scan_frequency=50, scan_direction=Constants.SCAN_DIRECTION))

        handle_front = self.sensor_front.request_handle_tcp(max_num_points_scan=600)
        handle_right = self.sensor_right.request_handle_tcp(max_num_points_scan=600)
        handle_left = self.sensor_left.request_handle_tcp(max_num_points_scan=600)
        handle_top = self.sensor_top.request_handle_tcp(max_num_points_scan=600)

        sensors_port = {
            Constants.SENSOR_FRONT_IP: handle_front["data"].get("port", None),
            Constants.SENSOR_RIGHT_IP: handle_right["data"].get("port", None),
            Constants.SENSOR_LEFT_IP: handle_left["data"].get("port", None),
            Constants.SENSOR_TOP_IP: handle_top["data"].get("port", None),
        }

        addresses = [f"{ip}:{port}" for ip, port in sensors_port.items() if port]
        print(addresses)

        if not addresses:
            return

        self.rust_exec = Popen(["./rust/client_tcp.exe", output_folder] + addresses)

        print(self.sensor_front.start_scanoutput())
        print(self.sensor_right.start_scanoutput())
        print(self.sensor_left.start_scanoutput())
        print(self.sensor_top.start_scanoutput())

    def stop_scan(self):
        if self.rust_exec is None:
            return

        print(self.sensor_front.stop_scanoutput())
        print(self.sensor_right.stop_scanoutput())
        print(self.sensor_left.stop_scanoutput())
        print(self.sensor_top.stop_scanoutput())

        print(self.sensor_front.release_handle())
        print(self.sensor_right.release_handle())
        print(self.sensor_left.release_handle())
        print(self.sensor_top.release_handle())

        self.rust_exec.wait()
        self.rust_exec = None
