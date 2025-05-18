import os
import torch
import numpy as np
from torch.utils.data import Dataset
from src.constants import PREPROCESSED_DIR


class SemanticKITTIDataset(Dataset):
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
