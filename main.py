import sys
import json
from time import sleep

import src.constants as constants
from src.SensorManager import SensorManager
from src.SensorReceiver import SensorReceiver
from src.LivePointCloudPlot import LivePointCloudPlot
from src.common.plot_point_cloud import plot_point_cloud

sys.path.append("src")
sys.path.append("src/common")
sys.path.append("src/interface")


def main():
    # sensor_front = SensorManager(constants.SENSOR_IP_FRONT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_right = SensorManager(constants.SENSOR_IP_RIGHT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_left = SensorManager(constants.SENSOR_IP_LEFT, constants.SERVER_IP, constants.SERVER_PORT)
    # sensor_top = SensorManager(constants.SENSOR_IP_TOP, constants.SERVER_IP, constants.SERVER_PORT)

    # print(print(sensor_top.set_parameters(samples_per_scan=600, scan_frequency=40)))
    # print(json.dumps(sensor_top.get_parameters(), sort_keys=True, indent=4))

    receiver = SensorReceiver("192.168.80.112", constants.SERVER_PORT)
    plot = LivePointCloudPlot(receiver.queue)

    plot.start()
    receiver.start()

    # print(sensor_top.request_handle_udp(max_num_points_scan=300, skip_scans=30))
    # print(sensor_top.start_scanoutput())

    # sleep(1)
    input("press any key to stop...")

    # print(sensor_top.stop_scanoutput())
    # print(sensor_top.release_handle())

    receiver.stop()

    # q = receiver.queue
    # print(q.qsize())
    # xyz = [[xy[0], xy[1], 0] for _ in range(q.qsize()) for xy in q.get()["xy"]]
    # print(q.qsize())
    # print(len(xyz))
    # plot_point_cloud(xyz)


if __name__ == "__main__":
    main()
