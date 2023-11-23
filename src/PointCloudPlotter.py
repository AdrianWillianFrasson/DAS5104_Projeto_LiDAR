import open3d as o3d
from multiprocessing import Process

from src.VolumeCalculator import VolumeCalculator


class PointCloudPlotter():

    def start(self, xyz: list):
        self.process = Process(target=self.run, args=(xyz,), daemon=True)
        self.process.start()

    def stop(self):
        self.process.terminate()

    @staticmethod
    def run(xyz: list):
        volume_calculator = VolumeCalculator()

        # _, mesh_ball = volume_calculator.ball_pivoting(xyz.copy())
        # _, mesh_alpha = volume_calculator.alpha_shapes(xyz.copy())
        _, convex_hull = volume_calculator.convex_hull(xyz.copy())
        _, delaunay = volume_calculator.delaunay(xyz.copy())

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        o3d.visualization.draw([pcd, convex_hull, delaunay])
