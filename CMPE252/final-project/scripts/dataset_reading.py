import os
import numpy as np

from src.utils.data_parser import parse_label_file, parse_velodyne_bin
from src.utils.visualize import visualize_point_cloud
from src.constants import DATASET_DIR

SEQUENCE = "00"
SAMPLE_IDX = 0
sequence_dir_path = os.path.join(DATASET_DIR, "sequences", SEQUENCE)

sequence_point_clouds = sorted(os.listdir(os.path.join(sequence_dir_path, "velodyne")))
sequence_labels = sorted(os.listdir(os.path.join(sequence_dir_path, "labels")))

print(f"--> SemanticKITTI sequence {SEQUENCE} contents")
print(f"Velodyne File Names: {sequence_point_clouds[:3]}")
print(f"Label File Names: {sequence_labels[:3]}")

print(f"\n--> Loading sample {SAMPLE_IDX} in sequence {SEQUENCE}")
sample_pcd = parse_velodyne_bin(
    os.path.join(sequence_dir_path, "velodyne", sequence_point_clouds[SAMPLE_IDX])
)
sample_semantic_ids, sample_instance_ids = parse_label_file(
    os.path.join(sequence_dir_path, "labels", sequence_labels[SAMPLE_IDX])
)

print(f"\n--> Data in first 3 scenes in sequence {SEQUENCE}")
print(sample_pcd[:3])
print(sample_semantic_ids[:3])
print(sample_instance_ids[:3])


print(f"\n--> Data overview of sample {SAMPLE_IDX} in sequence {SEQUENCE}")
print("Class distribution:")
unique, counts = np.unique(sample_semantic_ids, return_counts=True)
for cls_id, count in zip(unique, counts):
    print(f"Class {cls_id:2d}:\t{count} points")

print("\nMin/Max values for all dimensions in sample")
print(
    (np.min(sample_pcd[:, 0]), np.max(sample_pcd[:, 0])),
    (np.min(sample_pcd[:, 1]), np.max(sample_pcd[:, 1])),
    (np.min(sample_pcd[:, 2]), np.max(sample_pcd[:, 2])),
)

print(f"\n-->Rendering point cloud data...")
visualize_point_cloud("Data Reading", sample_pcd, sample_semantic_ids)
