class Constants():

    SERVER_IP = "192.168.1.50"
    SERVER_PORT = 6969

    SENSOR_FRONT_IP = "192.168.1.10"
    SENSOR_RIGHT_IP = "192.168.1.11"
    SENSOR_LEFT_IP = "192.168.1.12"
    SENSOR_TOP_IP = "192.168.1.13"

    SCANS_DIRECTORY = "./pointcloud/"
    SCAN_DIRECTION = "ccw"

    SENSOR_TOP_HEIGHT = 2350

    # [x, y, z]
    SENSOR_RIGHT_TRANSLATION = (1070, 1160, 0)
    SENSOR_LEFT_TRANSLATION = (1105, -1130, 0)

    # Euler angles [x, y, z]
    SENSOR_RIGHT_ROTATION = (0, 0, 0)
    SENSOR_LEFT_ROTATION = (0, 0, 0)

    BOUNDARIES_PROFILE_X_MIN = 100
    BOUNDARIES_PROFILE_X_MAX = 2370
    BOUNDARIES_PROFILE_Y_MIN = -1000
    BOUNDARIES_PROFILE_Y_MAX = 1000

    BOUNDARIES_ZAXIS_X_MIN = -2000
    BOUNDARIES_ZAXIS_X_MAX = 0
    BOUNDARIES_ZAXIS_Y_MIN = -3000
    BOUNDARIES_ZAXIS_Y_MAX = 900
