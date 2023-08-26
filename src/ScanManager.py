from subprocess import Popen

import src.constants as constants
from src.SensorManager import SensorManager


class ScanManager():

    def __init__(self):
        self.sensor_front = SensorManager(constants.SENSOR_IP_FRONT, constants.SERVER_IP, constants.SERVER_PORT)
        self.sensor_right = SensorManager(constants.SENSOR_IP_RIGHT, constants.SERVER_IP, constants.SERVER_PORT)
        self.sensor_left = SensorManager(constants.SENSOR_IP_LEFT, constants.SERVER_IP, constants.SERVER_PORT)
        self.sensor_top = SensorManager(constants.SENSOR_IP_TOP, constants.SERVER_IP, constants.SERVER_PORT)

    def start(self, output_folder: str):
        self.server = Popen([
            "./rust/server_tcp.exe",
            f"{constants.SERVER_IP}:{constants.SERVER_PORT}",
            output_folder,
        ])

        # self.sensor_front.request_handle_tcp()
        # self.sensor_top.request_handle_tcp()
        # self.sensor_front.start_scanoutput()
        # self.sensor_top.start_scanoutput()

    def stop(self):
        # self.sensor_front.stop_scanoutput()
        # self.sensor_top.stop_scanoutput()
        # self.sensor_front.release_handle()
        # self.sensor_top.release_handle()

        self.server.terminate()
        self.server.wait()
