# console.py
import os
import importlib


def import_all_classes_from_src():
    # This will contain all classes dynamically imported from the 'src' directory
    context = {}

    # List all modules in the 'src' directory
    modules = [f[:-3] for f in os.listdir('src') if f.endswith('.py') and f != '__init__.py']

    for module_name in modules:
        # Dynamically import module
        module = importlib.import_module(f'src.{module_name}')

        # Add classes from module to context
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            # Add only classes to the context (you can add additional filtering here if needed)
            if isinstance(attr, type):
                context[attr_name] = attr

    return context


def launch_shell(predefined_vars):
    # Ensure IPython is available
    try:
        from IPython import start_ipython
    except ImportError:
        raise ValueError("Please install IPython to use this shell.")

    # Merge predefined variables with the dynamically imported classes
    context = {**predefined_vars, **import_all_classes_from_src()}

    # Start the interactive shell
    start_ipython(argv=[], user_ns=context)


if __name__ == "__main__":
    import numpy as np
    import open3d as o3d
    from src.Constants import Constants
    from src.Reconstructor3D import Reconstructor3D
    scan_path = "./pointcloud/caixa_grande_2/"
    
    rec = Reconstructor3D()
    top_data = rec.process_data(scan_path, "top")
    # left_data = rec.process_data(scan_path, "left")
    # right_data = rec.process_data(scan_path, "right")
    # front_data = rec.process_data(scan_path, "front")

    def plot_data(data):
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(data)
        pcd.estimate_normals()
        o3d.visualization.draw([pcd])

    # Creating a dictionary of predefined variables and modules
    predefined_vars = {
        'np': np,
        'o3d': o3d,
        'scan_path': scan_path,
        'plot_data': plot_data,
        # 'joined_data': joined_data,
        'top_data': top_data,
        # 'right_data': right_data,
        # 'left_data': left_data
    }

    launch_shell(predefined_vars)

# aligner = PointCloudAligner()
# aligned_points = aligner.align(top_data, right_data, left_data)
# plot_data(aligned_points)
