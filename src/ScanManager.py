from subprocess import Popen

from src.Constants import Constants
from src.SensorManager import SensorManager


class ScanManager():

    def __init__(self):
        self.sensor_front = SensorManager(Constants.SENSOR_IP_FRONT, Constants.SERVER_IP, Constants.SERVER_PORT)
        self.sensor_right = SensorManager(Constants.SENSOR_IP_RIGHT, Constants.SERVER_IP, Constants.SERVER_PORT)
        self.sensor_left = SensorManager(Constants.SENSOR_IP_LEFT, Constants.SERVER_IP, Constants.SERVER_PORT)
        self.sensor_top = SensorManager(Constants.SENSOR_IP_TOP, Constants.SERVER_IP, Constants.SERVER_PORT)

        self.server_port = Constants.SERVER_PORT
        self.server_ip = Constants.SERVER_IP

    def start(self, output_folder: str):
        # print(self.sensor_front.set_parameters(samples_per_scan=600, scan_frequency=40))
        # print(self.sensor_right.set_parameters(samples_per_scan=600, scan_frequency=40))
        # print(self.sensor_left.set_parameters(samples_per_scan=600, scan_frequency=40))
        # print(self.sensor_top.set_parameters(samples_per_scan=600, scan_frequency=40))

        sensors_port = {
            Constants.SENSOR_IP_FRONT:
                self.sensor_front.request_handle_tcp(max_num_points_scan=600, skip_scans=35)["data"].get("port", None),
            Constants.SENSOR_IP_RIGHT:
                self.sensor_right.request_handle_tcp(max_num_points_scan=600, skip_scans=35)["data"].get("port", None),
            Constants.SENSOR_IP_LEFT:
                self.sensor_left.request_handle_tcp(max_num_points_scan=600, skip_scans=35)["data"].get("port", None),
            Constants.SENSOR_IP_TOP:
                self.sensor_top.request_handle_tcp(max_num_points_scan=600, skip_scans=35)["data"].get("port", None),
        }

        addresses = [f"{ip}:{port}" for ip, port in sensors_port.items() if port]

        self.server = Popen(["./rust/client_tcp.exe", output_folder] + addresses)

        # self.sensor_front.start_scanoutput()
        # self.sensor_right.start_scanoutput()
        # self.sensor_left.start_scanoutput()
        # self.sensor_top.start_scanoutput()

    def stop(self):
        # self.sensor_front.stop_scanoutput()
        # self.sensor_right.stop_scanoutput()
        # self.sensor_left.stop_scanoutput()
        # self.sensor_top.stop_scanoutput()

        # self.sensor_front.release_handle()
        # self.sensor_right.release_handle()
        # self.sensor_left.release_handle()
        # self.sensor_top.release_handle()

        # self.server.terminate()
        self.server.wait()
