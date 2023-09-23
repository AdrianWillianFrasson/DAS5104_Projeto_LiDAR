import numpy as np
from scipy.spatial import ConvexHull


class VolumeCalculator():

    def calculate(self, data_path: str) -> float:
        xyz = np.load(data_path)["xyz"]

        # real_volume_caixa = 79 * 77 * 50.2 = 305366.6
        hull = ConvexHull(xyz)
        volume = hull.volume

        return volume
