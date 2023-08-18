import open3d as o3d


def plot_3d(xyz):
    """xyz: numpy-3D-matrix"""

    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    o3d.visualization.draw_geometries([pcd])
