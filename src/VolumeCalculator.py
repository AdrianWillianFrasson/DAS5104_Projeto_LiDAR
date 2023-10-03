import numpy as np
import open3d as o3d

from math import pi
from scipy.spatial import Delaunay
from functools import reduce


def transform(points, rotation: tuple[int, int, int], translation: tuple[int, int, int]):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)

    if rotation != (0, 0, 0):
        rotation_matrix = pcd.get_rotation_matrix_from_xyz(rotation)
        pcd.rotate(rotation_matrix, center=(0, 0, 0))

    if translation != (0, 0, 0):
        pcd.translate(translation)

    return np.asarray(pcd.points)


def get_triangles_vertices(triangles, vertices):
    triangles_vertices = []

    for triangle in triangles:
        new_triangles_vertices = [vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]]
        triangles_vertices.append(new_triangles_vertices)

    return np.array(triangles_vertices)


def volume_under_triangle(triangle):
    p1, p2, p3 = triangle
    x1, z1, y1 = p1
    x2, z2, y2 = p2
    x3, z3, y3 = p3

    return abs((z1+z2+z3)*(x1*y2-x2*y1+x2*y3-x3*y2+x3*y1-x1*y3)/6)


class VolumeCalculator():

    def calculate(self, data_path: str) -> float:
        xyz = np.load(data_path)["xyz"]

        # ---------------------------------------------------------------------
        xyz = transform(xyz, [0, 0, -pi/2], [0, 2350, 0])

        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        # hull, _ = pcd.compute_convex_hull()
        # hull.orient_triangles()

        # volume = hull.get_volume() / 1000  # [mm^3] -> [cm^3]

        downpdc = pcd.voxel_down_sample(voxel_size=30)
        xyz = np.asarray(downpdc.points)
        xy_catalog = []

        for point in xyz:
            xy_catalog.append([point[0], point[2]])

        tri = Delaunay(np.array(xy_catalog))

        surface = o3d.geometry.TriangleMesh()
        surface.vertices = o3d.utility.Vector3dVector(xyz)
        surface.triangles = o3d.utility.Vector3iVector(tri.simplices)

        o3d.visualization.draw([downpdc, surface])

        volume = reduce(lambda a, b:  a + volume_under_triangle(b),
                        get_triangles_vertices(surface.triangles, surface.vertices), 0)

        print(round(volume, 4))
        # ---------------------------------------------------------------------
        # Volume Real (Caixa) = 79 * 77 * 50.2 = 305366.6 [cm^3]
        return round(volume)
