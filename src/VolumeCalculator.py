import numpy as np
import open3d as o3d
from scipy.spatial import Delaunay
from functools import reduce


class VolumeCalculator():

    def convex_hull(self, xyz):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.estimate_normals()

        hull, _ = pcd.compute_convex_hull()
        hull.orient_triangles()

        hull_ls = o3d.geometry.LineSet.create_from_triangle_mesh(hull)
        hull_ls.paint_uniform_color((1, 0, 0))

        volume = hull.get_volume()

        return volume, hull_ls

    def alpha_shapes(self, xyz):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.estimate_normals()

        alpha = 25

        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_alpha_shape(pcd, alpha)
        mesh.orient_triangles()

        return 1, mesh

    def ball_pivoting(self, xyz):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)
        pcd.estimate_normals()

        radii = [50, 25, 30]
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd, o3d.utility.DoubleVector(radii))

        # volume = mesh.get_volume()

        return 1, mesh

    def delaunay(self, xyz):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(xyz)

        xyz = np.asarray(pcd.points)
        xy_catalog = []

        for point in xyz:
            xy_catalog.append([point[0], point[2]])

        tri = Delaunay(np.array(xy_catalog))

        mesh = o3d.geometry.TriangleMesh()
        mesh.vertices = o3d.utility.Vector3dVector(xyz)
        mesh.triangles = o3d.utility.Vector3iVector(tri.simplices)

        volume = reduce(lambda a, b:  a + self._volume_under_triangle(b),
                        self._get_triangles_vertices(mesh.triangles, mesh.vertices), 0)

        return volume, mesh

    def _volume_under_triangle(self, triangle):
        p1, p2, p3 = triangle
        x1, z1, y1 = p1
        x2, z2, y2 = p2
        x3, z3, y3 = p3

        return abs((z1+z2+z3)*(x1*y2-x2*y1+x2*y3-x3*y2+x3*y1-x1*y3)/6)

    def _get_triangles_vertices(self, triangles, vertices):
        triangles_vertices = []

        for triangle in triangles:
            new_triangles_vertices = [vertices[triangle[0]], vertices[triangle[1]], vertices[triangle[2]]]
            triangles_vertices.append(new_triangles_vertices)

        return np.array(triangles_vertices)
