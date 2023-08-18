from math import cos, sin, pi


def polar_to_xy(distance: float, angle: float) -> tuple[float, float]:
    x = distance * cos(angle * pi / 180.0)
    y = distance * sin(angle * pi / 180.0)

    return x, y
