import numpy as np


def compute_iou(conf_matrix):
    # Compute mean IoU from confusion matrix
    intersection = np.diag(conf_matrix)
    ground_truth = conf_matrix.sum(axis=1)
    prediction = conf_matrix.sum(axis=0)
    union = ground_truth + prediction - intersection
    iou = np.divide(
        intersection,
        union,
        where=union != 0,
        out=np.zeros_like(intersection, dtype=float),
    )
    valid = (ground_truth != 0) & (prediction != 0)
    return np.mean(iou[valid])


def compute_pq(predictions, targets, num_classes):
    # Compute Panoptic Quality (PQ) for panoptic segmentation
    sq, rq, n = 0, 0, 0
    for cls in range(num_classes):
        pred_mask = predictions == cls
        gt_mask = targets == cls
        if gt_mask.sum() == 0 and pred_mask.sum() == 0:
            continue
        iou = (
            (pred_mask & gt_mask).sum() / (pred_mask | gt_mask).sum()
            if (pred_mask | gt_mask).sum() > 0
            else 0
        )
        sq += iou
        rq += (pred_mask.sum() > 0) and (gt_mask.sum() > 0)
        n += 1
    return sq / n if n > 0 else 0, rq / n if n > 0 else 0
