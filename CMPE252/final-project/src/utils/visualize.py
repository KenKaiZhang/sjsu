import numpy as np
import open3d as o3d

from src.constants import SEMANTIC_KITTI_ID_TO_INDEX, SEMANTIC_KITTI_COLORS


def visualize_point_cloud(title, points, semantic_ids, point_size=2.5):

    indices = np.vectorize(SEMANTIC_KITTI_ID_TO_INDEX.get)(semantic_ids, 0)
    colors = SEMANTIC_KITTI_COLORS[indices]
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])
    pcd.colors = o3d.utility.Vector3dVector(colors)

    vis = o3d.visualization.Visualizer()
    vis.create_window(window_name=title, width=1600, height=900)
    vis.add_geometry(pcd)
    opt = vis.get_render_option()
    opt.point_size = point_size
    vis.run()
    vis.destroy_window()
