import os
import numpy as np

from src.Reconstructor3D import Reconstructor3D
from src.VolumeCalculator import VolumeCalculator
from src.PointCloudPlotter import PointCloudPlotter


class DataManager():

    def __init__(self):
        self.point_cloud_plotter = PointCloudPlotter()
        self.volume_calculator = VolumeCalculator()
        self.reconstructor_3d = Reconstructor3D()

    def process_data(self, scan_path: str) -> float:
        # if os.path.isfile(f"{scan_path}data.npz"):
        #     xyz = np.load(f"{scan_path}data.npz")["xyz"]
        # else:
        xyz = self.reconstructor_3d.create_point_cloud(scan_path)
        np.savez_compressed(f"{scan_path}data.npz", xyz=xyz)

        # ---------------------------------------------------------------------
        # Volume Real (Caixa) = 79 * 77 * 50.2 = 305366.6 [cm^3]
        # volume_ball_pivoting, _ = self.volume_calculator.ball_pivoting(xyz.copy())
        # volume_alpha_shapes, _ = self.volume_calculator.alpha_shapes(xyz.copy())
        volume_convex_hull, _ = self.volume_calculator.convex_hull(xyz.copy())
        volume_delaunay, _ = self.volume_calculator.delaunay(xyz.copy())

        volume = volume_delaunay / 1000  # [mm^3] -> [cm^3]

        # print(f"ball: {volume_ball_pivoting}")
        # print(f"alph: {volume_alpha_shapes}")
        print(f"hull: {volume_convex_hull}")
        print(f"dlny: {volume_delaunay}")

        self.point_cloud_plotter.start(xyz)

        # ---------------------------------------------------------------------
        return round(volume, 2)
