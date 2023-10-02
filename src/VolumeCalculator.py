import numpy as np
import open3d as o3d
from scipy.spatial import ConvexHull
from math import pi

class VolumeCalculator():

    def calculate(self, data_path: str) -> float:
        xyz = np.load(data_path)["xyz"]

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

        # o3d_geometri_to_array = np.asarray(dcp_voxel.points)

        # real_volume_caixa = 79 * 77 * 50.2 = 305366.6
        hull, _ = dcp_voxel.compute_convex_hull()
        # hull_ls = o3d.geometry.LineSet.creat_from_tringle_mahs(hull)
        volume = hull.get_volume()/1000

        return volume
