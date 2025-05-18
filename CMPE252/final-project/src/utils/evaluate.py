import torch
import numpy as np


def compute_iou(pred, gt, num_classes=19):
    ious = []
    for cls in range(num_classes):
        pred_cls = pred == cls
        gt_cls = gt == cls
        intersection = (pred_cls & gt_cls).sum()
        union = (pred_cls | gt_cls).sum()
        if union > 0:
            ious.append(intersection / union)
    return np.mean(ious)
