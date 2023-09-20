import numpy as np


class PointCloudAligner:

    def __init__(self):
        # The rotation and translation matrices for the right sensor.
        # It's rotated around z-axis (which is the third row and column in the matrix) by -90 degrees.
        # self.rotation_right = np.array([
        #     [np.cos(np.deg2rad(-90)), -np.sin(np.deg2rad(-90)), 0],
        #     [np.sin(np.deg2rad(-90)), np.cos(np.deg2rad(-90)), 0],
        #     [0, 0, 1]
        # ])
        self.translation_right = np.array([1150, 1040, 0])

        self.rotation_right = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])
        # self.translation_right = np.array([0, 0, 0])

        # Similar matrices can be defined for the left sensor, but for the sake of the example,
        # we are only showing the matrices for the right sensor.

    def transform(self, points, rotation, translation):
        """
        Transforms a list of points using the given rotation and translation.
        """
        # Apply rotation
        rotated_points = np.dot(points, rotation.T)
        # Apply translation
        translated_points = rotated_points + translation
        return translated_points

    def align(self, top_points, right_points, left_points):
        """
        Aligns the point clouds from the top, right, and left sensors.
        """
        # The top points are the reference and don't need any transformation
        aligned_top = top_points

        # Transform the right points
        aligned_right = self.transform(right_points, self.rotation_right, self.translation_right)

        # Transform the left points if necessary (similar to right points)

        # Combine all the aligned point clouds
        combined_points = np.vstack((aligned_top, aligned_right))  # Add left points if necessary

        return combined_points
