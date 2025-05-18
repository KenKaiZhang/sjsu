import os
import numpy as np


def parse_label_file(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Label file {file_path} not found")

    labels = np.fromfile(file_path, dtype=np.uint32)

    semantic_labels = labels & 0xFFFF
    instance_ids = labels >> 16

    return semantic_labels, instance_ids


def parse_velodyne_bin(file_path):
    data = np.fromfile(file_path, dtype=np.float32)
    return data.reshape(-1, 4)
