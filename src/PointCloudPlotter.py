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
        dcp_radius, ind_radius = pcd.remove_radius_outlier(nb_points=10, radius=60)
        dcp_static, ind_static = dcp_radius.remove_statistical_outlier(nb_neighbors=60,
                                                                          std_ratio=0.7)
        dcp_voxel = dcp_static.voxel_down_sample(voxel_size=0.1)
        # dcp_uniform = dcp_radius.uniform_down_sample(1)
        # dcp_finus_radius, ind_finus_radius = dcp_voxel.remove_radius_outlier(nb_points=10, radius=60)
        rotation_matrix = dcp_voxel.get_rotation_matrix_from_xyz((0, 0, -pi/2))
        dcp_voxel.rotate(rotation_matrix, center=(0, 0, 0))

        # dcp_static.estimate_normals()
        # hull = dcp_static.compute_convex_hull()
        # radii = [10, 100, 1000]
        # mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(dcp_static, o3d.utility.DoubleVector(radii))

        # mesh, _ = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(dcp_static, depth=9)

        o3d.visualization.draw([dcp_voxel])
