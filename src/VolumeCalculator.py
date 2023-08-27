import numpy as np


class VolumeCalculator():

    def calculate(self, data_path: str) -> float:
        with open(data_path, "rb") as file:
            xyz = np.load(file)

        return 69.69
