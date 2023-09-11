import numpy as np


class VolumeCalculator():

    def calculate(self, data_path: str) -> float:
        xyz = np.load(data_path)["xyz"]
        # ---------------------------------------------------------------------

        # xyz = ...
        volume = 69.69

        # ---------------------------------------------------------------------
        return volume
