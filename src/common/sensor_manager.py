import requests


def get_parameters(sensor_address: str) -> dict:
    res = requests.get(f"http://{sensor_address}/cmd/get_parameter")
    return res.json()


def set_parameter(sensor_address: str, **params) -> dict:
    res = requests.get(f"http://{sensor_address}/cmd/set_parameter", params=params)
    return res.json()


def request_handle_udp(
    sensor_address: str,
    client_port: int,
    client_address: str = "192.168.1.50",
    watchdog: str = "off",  # Whether or not to use watchdog (on/off)
    watchdog_timeout: int = 60000,  # Timeout in ms if using watchdog
    packet_type: str = "A",
    start_angle: int = -1800000,
    max_num_points_scan: int = 0,
    skip_scans: int = 0,
) -> dict:

    params = {
        "address": client_address,
        "port": client_port,
        "packet_type": packet_type,
        "watchdog": watchdog,
        "watchdogtimeout": watchdog_timeout,
        "start_angle": start_angle,
        "max_num_points_scan": max_num_points_scan,
        "skip_scans": skip_scans,
    }

    res = requests.get(f"http://{sensor_address}/cmd/request_handle_udp", params=params)
    return res.json()


def release_handle(sensor_address: str, handle: str) -> dict:
    res = requests.get(f"http://{sensor_address}/cmd/release_handle?handle={handle}")
    return res.json()


def set_scanoutput_config(
    sensor_address: str,
    handle: str,
    watchdog: str = "off",  # Whether or not to use watchdog (on/off)
    watchdog_timeout: int = 60000,  # Timeout in ms if using watchdog
    packet_type: str = "A",
    start_angle: int = -1800000,
    max_num_points_scan: int = 0,
    skip_scans: int = 0,
) -> dict:

    params = {
        "handle": handle,
        "watchdog": watchdog,
        "watchdogtimeout": watchdog_timeout,
        "packet_type": packet_type,
        "start_angle": start_angle,
        "max_num_points_scan": max_num_points_scan,
        "skip_scans": skip_scans,
    }

    res = requests.get(f"http://{sensor_address}/cmd/set_scanoutput_config", params=params)
    return res.json()


def start_scanoutput(sensor_address: str, handle: str) -> dict:
    res = requests.get(f"http://{sensor_address}/cmd/start_scanoutput?handle={handle}")
    return res.json()


def stop_scanoutput(sensor_address: str, handle: str) -> dict:
    res = requests.get(f"http://{sensor_address}/cmd/stop_scanoutput?handle={handle}")
    return res.json()
