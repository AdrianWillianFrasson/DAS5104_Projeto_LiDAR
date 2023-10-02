class Constants():

    SERVER_IP = "192.168.1.50"
    SERVER_PORT = 6969

    SENSOR_FRONT_IP = "192.168.1.10"
    SENSOR_RIGHT_IP = "192.168.1.11"
    SENSOR_LEFT_IP = "192.168.1.12"
    SENSOR_TOP_IP = "192.168.1.13"

    # [x, y, z]
    SENSOR_RIGHT_TRANSLATION = (1070, 1160, 0)
    SENSOR_LEFT_TRANSLATION = (1105, -1130, 0)

    # Euler angles [xyz]
    SENSOR_RIGHT_ROTATION = (0, 0, 0)
    SENSOR_LEFT_ROTATION = (0, 0, 0)

    # Bounding box
    BOUNDING_BOX_PROFILE_X_MIN = 500
    BOUNDING_BOX_PROFILE_X_MAX = 2370
    BOUNDING_BOX_PROFILE_Y_MIN = -1000
    BOUNDING_BOX_PROFILE_Y_MAX = 1000

    # Speed Bounding box
    BOUNDING_BOX_SPEED_X_MIN = -2000
    BOUNDING_BOX_SPEED_X_MAX = 0
    BOUNDING_BOX_SPEED_Y_MIN = -3000
    BOUNDING_BOX_SPEED_Y_MAX = 900

    SCAN_DIRECTION = "ccw"
