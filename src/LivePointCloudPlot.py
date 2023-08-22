from threading import Thread
import open3d as o3d
import numpy as np

from src.SafeList import SafeList


class LivePointCloudPlot(Thread):

    def __init__(self, queue: SafeList):
        super().__init__(daemon=True)
        self.queue = queue

    def run(self):
        vis = o3d.visualization.VisualizerWithKeyCallback()

        vis.create_window("?", width=1080, height=720)
        vis.register_key_callback(ord("C"), self.key_c)
        vis.register_key_callback(ord("V"), self.key_v)

        vis.get_render_option().point_size = 5
        self.set_view_range(vis, 1500)

        vis.register_animation_callback(self.animation)

        vis.run()
        vis.destroy_window()

    def animation(self, vis):
        data = self.queue.get_all()

        if not len(data):
            return

        self.pcd.points = o3d.utility.Vector3dVector(np.concatenate((
            np.asarray(self.pcd.points),
            [[xy[0], xy[1], 0] for points in data for xy in points["xy"]]
        )))

        print(self.queue.size())
        vis.update_geometry(self.pcd)
        # vis.poll_events()
        # vis.update_renderer()

    def set_view_range(self, vis, axis_range: int):
        self.pcd = o3d.geometry.PointCloud()
        self.pcd.points = o3d.utility.Vector3dVector(np.array([
            [1.0, 1.0, 0.0],
            [-1.0, 1.0, 0.0],
            [-1.0, -1.0, 0.0],
            [1.0, -1.0, 0.0],
        ]) * axis_range)

        vis.add_geometry(self.pcd)
        self.pcd.points = o3d.utility.Vector3dVector([])

    def key_c(self, vis):
        self.pcd.points = o3d.utility.Vector3dVector([])

    def key_v(self, vis):
        print(np.asarray(self.pcd.points).shape)
