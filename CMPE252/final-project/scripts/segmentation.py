import os
import numpy as np
import open3d as o3d
import pandas as pd
from matplotlib import pyplot as plt

from src.utils.data_parser import parse_label_file, parse_velodyne_bin
from src.constants import DATASET_DIR

SEQUENCE = "00"

sample_velodyne_dir = os.path.join(DATASET_DIR, "sequences", SEQUENCE, "velodyne")
sample_labels_dir = os.path.join(DATASET_DIR, "sequences", SEQUENCE, "labels")

sample_velodyne_files = os.listdir(sample_velodyne_dir)
sample_labels_files = os.listdir(sample_labels_dir)

sample_pcd = parse_velodyne_bin(
    os.path.join(sample_velodyne_dir, sample_velodyne_files[0])
)
semantic_id, instance_id = parse_label_file(
    os.path.join(sample_labels_dir, sample_labels_files[0])
)

sample_point_cloud = o3d.geometry.PointCloud()
sample_point_cloud.points = o3d.utility.Vector3dVector(sample_pcd[:, :3])

print(f"\n-->RANSAC Segmentation")
plane_model, inliers = sample_point_cloud.segment_plane(
    distance_threshold=0.3, ransac_n=3, num_iterations=150
)

# Identify inlier points -> road
inlier_cloud = sample_point_cloud.select_by_index(inliers)
inlier_cloud.paint_uniform_color([0, 1, 1])
print("Road objects identified...")

# Identify outlier points -> objects on the road
outlier_cloud = sample_point_cloud.select_by_index(inliers, invert=True)
outlier_cloud.paint_uniform_color([1, 0, 0])
print("On road objects identified...")

# visualize the components
o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud], width=1600, height=900)

print("\n--> DBSCAN clustering")
o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug)
labels = np.array(outlier_cloud.cluster_dbscan(eps=0.45, min_points=10))
max_label = labels.max()
print(f"{max_label + 1} clusters detected...")

# Get label colors
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
colors[labels < 0] = 0

# Colorized objects on the road
outlier_cloud.colors = o3d.utility.Vector3dVector(colors[:, :3])
o3d.visualization.draw_geometries([outlier_cloud], width=1600, height=900)

print("\n--> Generating 3D Bounding Boxes")
objects = []
indexes = pd.Series(range(len(labels))).groupby(labels, sort=False).apply(list).tolist()

MAX_POINTS = 300
MIN_POINTS = 25

for i in range(0, len(indexes)):
    nb_points = len(outlier_cloud.select_by_index(indexes[i]).points)
    if nb_points > MIN_POINTS and nb_points < MAX_POINTS:
        sub_cloud = outlier_cloud.select_by_index(indexes[i])
        obb = sub_cloud.get_axis_aligned_bounding_box()
        obb.color = (1, 0, 0)  # R, G, B
        objects.append(obb)

print(f"Number of Bounding Boxes calculated {len(objects)}")
print(f"Number of predicted bounding box: {len(objects)}")

list_of_visuals = []
list_of_visuals.append(outlier_cloud)
list_of_visuals.extend(objects)
list_of_visuals.append(inlier_cloud)

o3d.visualization.draw_geometries(list_of_visuals, width=1600, height=900)
