import numpy as np
import open3d as o3d
from multiprocessing import Process, Queue


class PointCloudLivePlotter():

    def start(self, queue: Queue):
        self.process = Process(target=self.run, args=(queue,), daemon=True)
        self.process.start()

    def stop(self):
        self.process.terminate()

    @staticmethod
    def run(queue: Queue):
        plotter = Plotter(queue)
        plotter.plot_forever()


class Plotter():

    def __init__(self, queue: Queue):
        self.vis = o3d.visualization.VisualizerWithKeyCallback()
        self.pcd = o3d.geometry.PointCloud()
        self.queue = queue

        self.vis.create_window("?", width=1080, height=720)
        self.vis.register_key_callback(ord("C"), self.key_c)
        self.vis.register_key_callback(ord("V"), self.key_v)

        self.vis.get_render_option().point_size = 5
        self.set_view_range(1500)

        self.vis.register_animation_callback(self.animation)

    def plot_forever(self):
        self.vis.run()
        self.vis.destroy_window()

    def animation(self, _):
        data = []

        try:
            for _ in range(self.queue.qsize()):
                data.extend(self.queue.get(False)["xy"])
        except Exception:
            # print("queue.get() error...")
            pass

        if not len(data):
            return

        self.pcd.points = o3d.utility.Vector3dVector(np.concatenate((
            np.asarray(self.pcd.points),
            [[xy[0], xy[1], 0] for xy in data]
        )))

        # print(self.queue.qsize())
        self.vis.update_geometry(self.pcd)
        # self.vis.poll_events()
        # self.vis.update_renderer()

    def set_view_range(self, axis_range: int):
        self.pcd.points = o3d.utility.Vector3dVector(np.array([
            [1.0, 1.0, 0.0],
            [-1.0, 1.0, 0.0],
            [-1.0, -1.0, 0.0],
            [1.0, -1.0, 0.0],
        ]) * axis_range)

        self.vis.add_geometry(self.pcd)
        self.pcd.points = o3d.utility.Vector3dVector([])

    def key_c(self, _):
        self.pcd.points = o3d.utility.Vector3dVector([])

    def key_v(self, _):
        print(np.asarray(self.pcd.points).shape)
