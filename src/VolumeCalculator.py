import numpy as np
import open3d as o3d


class VolumeCalculator():

    def calculate(self, data_path: str) -> float:
        xyz = np.load(data_path)["xyz"]

        # ---------------------------------------------------------------------
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        hull, _ = pcd.compute_convex_hull()
        hull.orient_triangles()

        volume = hull.get_volume() / 1000  # [mm^3] -> [cm^3]

        # ---------------------------------------------------------------------
        # Volume Real (Caixa) = 79 * 77 * 50.2 = 305366.6 [cm^3]
        return round(volume)
