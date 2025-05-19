import os
import torch
import numpy as np
from torch.utils.data import Dataset

from src.utils.data_parser import *


class SemanticKITTIPreprocessedDataset(Dataset):
    def __init__(self, dataset, sequences):
        self.files = []
        for seq in sequences:
            seq_dir = os.path.join(dataset, "sequences", seq)
            self.files.extend(
                [
                    os.path.join(seq_dir, f)
                    for f in os.listdir(seq_dir)
                    if f.endswith(".npy")
                ]
            )

    def __len__(self):
        return len(self.files)

    def __getitem__(self, idx):
        data = np.load(self.files[idx], allow_pickle=True).item()
        voxel_points = data["voxel_points"].astype(
            np.float32
        )  # [N, 4] (x, y, z, intensity)
        voxel_semantic_ids = data["voxel_semantic_ids"].astype(np.int64)  # [N]
        voxel_instance_ids = data["voxel_instance_ids"].astype(np.int64)  # [N]

        return {
            "points": torch.from_numpy(voxel_points),
            "semantic_labels": torch.from_numpy(voxel_semantic_ids),
            "instance_labels": torch.from_numpy(voxel_instance_ids),
        }


class SemanticKITTIDataset(Dataset):
    def __init__(self, dataset_dir, sequences):
        self.dataset_dir = dataset_dir
        self.sequences = sequences
        self.files = []
        
        # Load file paths
        for seq in sequences:
            seq_dir = os.path.join(dataset_dir, 'sequences', seq)
            velodyne_dir = os.path.join(seq_dir, 'velodyne')
            labels_dir = os.path.join(seq_dir, 'labels')
            
            if not os.path.exists(velodyne_dir) or not os.path.exists(labels_dir):
                continue
                
            scans = sorted(os.listdir(velodyne_dir))
            for scan in scans:
                if scan.endswith('.bin'):
                    scan_id = scan[:-4]
                    point_path = os.path.join(velodyne_dir, scan)
                    label_path = os.path.join(labels_dir, f"{scan_id}.label")
                    if os.path.exists(label_path):
                        self.files.append((point_path, label_path))
        
        print(f"Loaded {len(self.files)} scans from sequences {sequences}")
    
    def __len__(self):
        return len(self.files)
    
    def __getitem__(self, idx):
        point_path, label_path = self.files[idx]
        
        points = parse_velodyne_bin(point_path)
        semantic_labels, instance_labels = parse_label_file(label_path)
        
        return {
            'points': torch.from_numpy(points).float(),  # Shape: (n_points, 4)
            'semantic_labels': torch.from_numpy(semantic_labels.astype(np.int32)).long(),
            'instance_labels': torch.from_numpy(instance_labels.astype(np.int32)).long()
        }