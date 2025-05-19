import numpy as np
import open3d as o3d

from src.constants import SEMANTIC_KITTI_ID_TO_INDEX


def remap_labels(semantic_labels):
    mapped_labels = np.zeros_like(semantic_labels)
    for raw_label, mapped_label in SEMANTIC_KITTI_ID_TO_INDEX.items():
        mapped_labels[semantic_labels == raw_label] = mapped_label
    return mapped_labels


def augment_points(
    points, rotation_min, rotation_max, translation_min, translation_max
):
    points_aug = points.copy()

    # Rotation
    theta = np.random.uniform(rotation_min, rotation_max)
    rotation_matrix = np.array(
        [
            [np.cos(theta), -np.sin(theta), 0],
            [np.sin(theta), np.cos(theta), 0],
            [0, 0, 1],
        ]
    )
    points_aug[:, :3] = points_aug[:, :3] @ rotation_matrix

    # Translation
    translation = np.random.uniform(translation_min, translation_max, 3)
    points_aug[:, :3] += translation
    return points_aug


def normalize_point_cloud(points):
    points_normalized = points.copy()
    centroid = np.mean(points_normalized[:, :3], axis=0)
    points_normalized[:, :3] = points_normalized[:, :3] - centroid
    return points_normalized, centroid


def voxelize_point_cloud(points, voxel_size):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:, :3])

    voxel_grid = o3d.geometry.VoxelGrid.create_from_point_cloud(
        pcd, voxel_size=voxel_size
    )
    voxel_points = np.array(
        [
            voxel_grid.origin + voxel.grid_index * voxel_size + voxel_size / 2
            for voxel in voxel_grid.get_voxels()
        ]
    )

    if points.shape[1] > 3:
        voxel_features = np.zeros((len(voxel_points), points.shape[1]))
        voxel_features[:, :3] = voxel_points
        voxel_features[:, 3:] = points[0, 3:]
    else:
        voxel_features = voxel_points

    return voxel_features, np.array(
        [voxel.grid_index for voxel in voxel_grid.get_voxels()]
    )


def assign_voxel_labels(
    original_points, voxel_points, original_semantic_ids, original_instance_ids
):
    original_pcd = o3d.geometry.PointCloud()
    original_pcd.points = o3d.utility.Vector3dVector(original_points[:, :3])
    voxel_pcd = o3d.geometry.PointCloud()
    voxel_pcd.points = o3d.utility.Vector3dVector(voxel_points[:, :3])

    kdtree = o3d.geometry.KDTreeFlann(original_pcd)
    voxel_semantic_ids = np.zeros(len(voxel_points), dtype=np.uint32)
    voxel_instance_ids = np.zeros(len(voxel_points), dtype=np.uint32)

    for i in range(len(voxel_points)):
        [_, idx, _] = kdtree.search_knn_vector_3d(voxel_pcd.points[i], 1)
        voxel_semantic_ids[i] = original_semantic_ids[idx[0]]
        voxel_instance_ids[i] = original_instance_ids[idx[0]]

    return voxel_semantic_ids, voxel_instance_ids


def add_noise(points, noise_std):
    noise = np.random.normal(0, noise_std, points[:, :3].shape)
    points_noise = points.copy()
    points_noise[:, :3] += noise
    return points_noise
