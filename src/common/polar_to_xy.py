from math import cos, sin, pi


def polar_to_xy(distances: list, first_angle: int, angular_increment: int) -> list[tuple[float, float]]:
    first_angle /= 10000
    angular_increment /= 10000

    xy = []

    for i, distance in enumerate(distances):
        angle = (first_angle + i * angular_increment) * pi / 180.0

        x = round(distance * cos(angle))
        y = round(distance * sin(angle))

        xy.append((x, y))

    return xy
