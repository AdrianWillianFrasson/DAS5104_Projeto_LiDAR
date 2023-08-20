import sys

import src.constants as constants
from src.SensorManager import SensorManager
from src.SensorReceiver import SensorReceiver
from src.common.plot_point_cloud import plot_point_cloud

sys.path.append("src")
sys.path.append("src/common")
sys.path.append("src/interface")


def main():
    # sensor_front = SensorManager(constants.SENSOR_IP_FRONT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_right = SensorManager(constants.SENSOR_IP_RIGHT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_left = SensorManager(constants.SENSOR_IP_LEFT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_top = SensorManager(constants.SENSOR_IP_TOP, constants.SERVER_IP, constants.SERVER_PORT)

    receiver = SensorReceiver("192.168.80.106", constants.SERVER_PORT)
    receiver.start()

    # print(sensor_front.request_handle_udp())
    # print(sensor_front.start_scanoutput())

    input("press any key to plot...")

    # print(sensor_front.stop_scanoutput())
    # print(sensor_front.release_handle())

    receiver.stop()

    xy = receiver.xy
    xyz = [[xy[i][0], xy[i][1], 0] for i in range(len(xy))]
    print(len(xyz))
    plot_point_cloud(xyz)


if __name__ == "__main__":
    main()
