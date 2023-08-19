from src.common.http_request import get
import src.constants as constants


class SensorManager():

    def __init__(self, sensor_ip: str, server_ip: str, server_port: int):
        self.sensor_ip = sensor_ip
        self.server_ip = server_ip
        self.server_port = server_port

        self.handle = ""

        # Default setting...
        self.set_parameters(scan_direction=constants.SCAN_DIRECTION)

    def get_parameters(self):
        return get(f"http://{self.sensor_ip}/cmd/get_parameter")

    def set_parameters(self, **params):
        return get(f"http://{self.sensor_ip}/cmd/set_parameter", params=params)

    def request_handle_udp(
        self,
        watchdog: str = "off",  # ["on", "off"]
        watchdogtimeout: int = 60000,  # [ms]
        packet_type: str = "A",  # ["A", "B", "C"]
        start_angle: int = 0,
        max_num_points_scan: int = 0,
        skip_scans: int = 0,
    ):

        params = {
            "address": self.server_ip,
            "port": self.server_port,
            "watchdog": watchdog,
            "watchdogtimeout": watchdogtimeout,
            "packet_type": packet_type,
            "start_angle": start_angle,
            "max_num_points_scan": max_num_points_scan,
            "skip_scans": skip_scans,
        }

        res = get(f"http://{self.sensor_ip}/cmd/request_handle_udp", params=params)

        if res["ok"]:
            self.handle = res["data"].get("handle", "")

        return res

    def release_handle(self):
        res = get(f"http://{self.sensor_ip}/cmd/release_handle", params={"handle": self.handle})

        self.handle = ""

        return res

    def set_scanoutput_config(
        self,
        watchdog: str = "off",  # ["on", "off"]
        watchdogtimeout: int = 60000,  # [ms]
        packet_type: str = "A",  # ["A", "B", "C"]
        start_angle: int = 0,
        max_num_points_scan: int = 0,
        skip_scans: int = 0,
    ):

        params = {
            "handle": self.handle,
            "watchdog": watchdog,
            "watchdogtimeout": watchdogtimeout,
            "packet_type": packet_type,
            "start_angle": start_angle,
            "max_num_points_scan": max_num_points_scan,
            "skip_scans": skip_scans,
        }

        return get(f"http://{self.sensor_ip}/cmd/set_scanoutput_config", params=params)

    def start_scanoutput(self):
        return get(f"http://{self.sensor_ip}/cmd/start_scanoutput", params={"handle": self.handle})

    def stop_scanoutput(self):
        return get(f"http://{self.sensor_ip}/cmd/stop_scanoutput", params={"handle": self.handle})
