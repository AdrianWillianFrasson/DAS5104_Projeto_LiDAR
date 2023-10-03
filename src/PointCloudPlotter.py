import numpy as np
import open3d as o3d
from multiprocessing import Process
from math import pi


class PointCloudPlotter():

    def start(self, data_path: str):
        self.process = Process(target=self.run, args=(data_path,), daemon=True)
        self.process.start()

    def stop(self):
        self.process.terminate()

    @staticmethod
    def run(data_path: str):
        xyz = np.load(data_path)["xyz"]

        # ---------------------------------------------------------------------
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        rotation_matrix = pcd.get_rotation_matrix_from_xyz((0, 0, -pi/2))
        pcd.rotate(rotation_matrix, center=(0, 0, 0))

        hull, _ = pcd.compute_convex_hull()
        hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
        hull_ls.paint_uniform_color((1, 0, 0))

        # ---------------------------------------------------------------------
        o3d.visualization.draw([pcd, hull_ls])
