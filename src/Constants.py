class Constants():
    # Verificar as imagens em ../assets/montagem/

    # Ethernet ----------------------------------------------------------------
    SERVER_IP = "192.168.1.50"  # Não necessário quando usado handle TCP
    SERVER_PORT = 6969          # Não necessário quando usado handle TCP

    SENSOR_FRONT_IP = "192.168.1.10"
    SENSOR_RIGHT_IP = "192.168.1.11"
    SENSOR_LEFT_IP = "192.168.1.12"
    SENSOR_TOP_IP = "192.168.1.13"

    # Scans -------------------------------------------------------------------
    SCANS_DIRECTORY = "./pointcloud/"
    SCAN_DIRECTION = "ccw"

    # Sensors -----------------------------------------------------------------
    SENSOR_TOP_HEIGHT = 2400

    # [x, y, z]
    SENSOR_RIGHT_TRANSLATION = (1070, 1160, 0)
    SENSOR_LEFT_TRANSLATION = (1105, -1130, 0)

    # Euler angles [x, y, z]
    SENSOR_RIGHT_ROTATION = (0, 0, 0)
    SENSOR_LEFT_ROTATION = (0, 0, 0)

    BOUNDARIES_PROFILE_X_MIN = 100
    BOUNDARIES_PROFILE_X_MAX = 2385
    BOUNDARIES_PROFILE_Y_MIN = -1000
    BOUNDARIES_PROFILE_Y_MAX = 1000

    BOUNDARIES_ZAXIS_X_MIN = -2300
    BOUNDARIES_ZAXIS_X_MAX = -400
    BOUNDARIES_ZAXIS_Y_MIN = -7000
    BOUNDARIES_ZAXIS_Y_MAX = -1750
