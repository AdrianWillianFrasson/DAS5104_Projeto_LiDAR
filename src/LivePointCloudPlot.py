from threading import Thread
from queue import Queue
from time import sleep
import open3d as o3d
import numpy as np


class LivePointCloudPlot(Thread):

    def __init__(self, queue: Queue):
        super().__init__(daemon=True)

        self.queue = queue

    def run(self):
        vis = o3d.visualization.VisualizerWithKeyCallback()

        vis.create_window("?", width=1080, height=720)
        vis.register_key_callback(ord("C"), self.key_c)

        vis.get_render_option().point_size = 5
        self.set_view_range(vis, 450)

        vis.register_animation_callback(self.animation)

        vis.run()
        vis.destroy_window()

    def animation(self, vis):
        try:
            data = self.queue.get(False)["xy"]
            self.pcd.points = o3d.utility.Vector3dVector(np.concatenate((
                np.asarray(self.pcd.points),
                [[xy[0], xy[1], 0] for xy in data]
            )))

            vis.update_geometry(self.pcd)
            # vis.poll_events()
            # vis.update_renderer()
            sleep(0.0)

        except Exception:
            sleep(0.0)

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
