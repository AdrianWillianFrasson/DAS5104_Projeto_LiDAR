import numpy as np
import open3d as o3d
from multiprocessing import Process


class PointCloudPlotter():

    def start(self, data_path: str):
        self.process = Process(target=self.run, args=(data_path,), daemon=True)
        self.process.start()

    def stop(self):
        self.process.terminate()

    @staticmethod
    def run(data_path: str):
        with open(data_path, "rb") as file:
            xyz = np.load(file)

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
        o3d.visualization.draw_geometries([pcd])
