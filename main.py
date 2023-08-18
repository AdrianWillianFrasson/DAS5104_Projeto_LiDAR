import sys
import time
import numpy as np

import src.constants as constants
from src.SensorManager import SensorManager
from src.SensorReceiver import SensorReceiver
from src.common.plot_3d import plot_3d

sys.path.append("src")
sys.path.append("src/common")
sys.path.append("src/interface")


def main():
    # sensor_front = SensorManager(constants.SENSOR_IP_FRONT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_right = SensorManager(constants.SENSOR_IP_RIGHT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_left = SensorManager(constants.SENSOR_IP_LEFT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_top = SensorManager(constants.SENSOR_IP_TOP, constants.SERVER_IP, constants.SERVER_PORT)

    # SensorReceiver.start()

    # print(sensor_front.request_handle_udp())
    # print(sensor_front.start_scanoutput())

    # time.sleep(5)

    # print(sensor_front.stop_scanoutput())
    # print(sensor_front.release_handle())

    # SensorReceiver.stop()

    xyz = np.random.rand(10000000, 3)
    plot_3d(xyz)


if __name__ == "__main__":
    main()
