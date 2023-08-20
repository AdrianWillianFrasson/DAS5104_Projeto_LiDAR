import open3d as o3d


def plot_point_cloud(xyz: list[list]):
    """xyz: [[x1, y1, z1], ...]"""

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    o3d.visualization.draw_geometries([pcd])
