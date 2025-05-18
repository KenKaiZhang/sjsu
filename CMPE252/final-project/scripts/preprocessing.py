import os
from tqdm import tqdm
from pathlib import Path

from src.utils.data_parser import *
from src.utils.preprocess import *
from src.constants import DATASET_DIR, PREPROCESSED_DIR, TRAIN_SEQUENCES

ROTATION = 0.1
TRANSLATION = 0.5
NOISE_STD = 0.01
VOXEL_SIZE = 0.3

print("--> Preprocessing SemanticKITTI")
for seq in TRAIN_SEQUENCES:

    # Locate data
    seq_dir = os.path.join(DATASET_DIR, "sequences", seq)
    velodyne_dir = os.path.join(seq_dir, "velodyne")
    labels_dir = os.path.join(seq_dir, "labels")

    # Locate output
    out_seq_dir = os.path.join(PREPROCESSED_DIR, "sequences", seq)
    os.makedirs(out_seq_dir, exist_ok=True)

    pcd_files = sorted(os.listdir(velodyne_dir))
    labels_files = sorted(os.listdir(labels_dir))

    for pcd_file, label_file in tqdm(
        zip(pcd_files, labels_files),
        total=min(len(pcd_files), len(labels_files)),
        desc=f"Processing files in seq {seq}",
    ):

        # Locate .bin and .label
        pcd_file_path = os.path.join(velodyne_dir, pcd_file)
        label_file_path = os.path.join(labels_dir, label_file)

        points = parse_velodyne_bin(pcd_file_path)
        semantic_ids, instance_ids = parse_label_file(label_file_path)

        # Remap semantic labels
        semantic_ids_mapped = remap_labels(semantic_ids)

        points_processed = points.copy()

        # Apply augmentations
        points_processed = augment_points(
            points_processed, -ROTATION, ROTATION, -TRANSLATION, TRANSLATION
        )

        # Apply noise
        points_processed = add_noise(points_processed, NOISE_STD)

        # Normalize
        points_normalized, centroid = normalize_point_cloud(points_processed)

        # Voxelize
        voxel_points, voxel_indices = voxelize_point_cloud(
            points_normalized, VOXEL_SIZE
        )

        # Assign labels to voxels
        voxel_semantic_ids, voxel_instance_ids = assign_voxel_labels(
            points_normalized, voxel_points, semantic_ids_mapped, instance_ids
        )

        preprocess_results = {
            "voxel_points": voxel_points,
            "voxel_semantic_ids": voxel_semantic_ids,
            "voxel_instance_ids": voxel_instance_ids,
            "voxel_indices": voxel_indices,
            "centroid": centroid,
            "original_points": points,
        }

        # Save results
        output_file = os.path.join(out_seq_dir, f"{Path(pcd_file).stem}.npy")
        np.save(output_file, preprocess_results)

print("Preprocessing complete")
