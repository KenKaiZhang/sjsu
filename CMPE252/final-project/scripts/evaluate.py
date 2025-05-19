import os
import torch
import numpy as np
from tqdm import tqdm
from torch.utils.data import DataLoader
from sklearn.metrics import confusion_matrix

from src.utils.evaluate import *
from src.utils.train import collate_fn
from src.models.simplemodel import SimpleModel
from src.utils.visualize import visualize_point_cloud
from src.datasets.semantickitti_dataset import SemanticKITTIDataset
from src.constants import (
    SEMANTIC_KITTI_ID_TO_INDEX,
    SAVED_MODELS_DIR,
    DATASET_DIR,
    VAL_SEQUENCES,
)

BATCH_SIZE = 4
INSTANCE_DIM = 32

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"--> Using {device}")

num_classes = len(SEMANTIC_KITTI_ID_TO_INDEX)
model_path = os.path.join(SAVED_MODELS_DIR, "simplemodel", "simplemodel.pth")

print(f"\n--> Loading model from {model_path}")
model = SimpleModel(instance_embedding_dim=INSTANCE_DIM).to(device)
model.load_state_dict(torch.load(model_path, map_location=device))

print(f"\n--> Loading validation dataset")
val_dataset = SemanticKITTIDataset(DATASET_DIR, VAL_SEQUENCES)
val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=4,
    collate_fn=collate_fn,
)

print("\n--> Validation start")
model.eval()
conf_matrix = np.zeros((num_classes, num_classes), dtype=np.int64)
total_pq, total_sq, total_rq = 0.0, 0.0, 0.0
num_samples = 0
sample_data = None

with torch.no_grad():
    for i, batch in enumerate(tqdm(val_loader, desc="Evaluating")):
        points = batch["points"].to(device)  # Shape: (batch_size, max_points, 4)
        semantic_gt = batch["semantic_labels"].to(
            device
        )  # Shape: (batch_size, max_points)
        instance_gt = batch["instance_labels"].to(
            device
        )  # Shape: (batch_size, max_points)
        masks = batch["masks"].to(device)  # Shape: (batch_size, max_points)

        # Forward pass
        semantic_pred, instance_pred = model(points)
        semantic_pred = torch.argmax(
            semantic_pred, dim=2
        )  # Shape: (batch_size, max_points)

        # Update confusion matrix for mIoU
        for b in range(points.shape[0]):
            mask = masks[b]  # Valid points
            pred = semantic_pred[b][mask].cpu().numpy()
            gt = semantic_gt[b][mask].cpu().numpy()
            if len(pred) > 0:  # Skip empty masks
                conf_matrix += confusion_matrix(
                    gt.flatten(), pred.flatten(), labels=np.arange(num_classes)
                )

        # Compute PQ for panoptic segmentation
        for b in range(points.shape[0]):
            mask = masks[b]
            pred = semantic_pred[b][mask].cpu().numpy()
            gt = semantic_gt[b][mask].cpu().numpy()
            if len(pred) > 0:
                sq, rq = compute_pq(pred, gt, num_classes)
                total_sq += sq
                total_rq += rq
                total_pq += sq * rq
                num_samples += 1

        # Save a sample for visualization
        if sample_data is None:
            mask = masks[0]
            sample_data = {
                "points": points[0][mask].cpu().numpy(),
                "semantic_pred": semantic_pred[0][mask].cpu().numpy(),
                "semantic_gt": semantic_gt[0][mask].cpu().numpy(),
            }

# Compute final metrics
mIoU = compute_iou(conf_matrix)
avg_pq = total_pq / num_samples if num_samples > 0 else 0.0
avg_sq = total_sq / num_samples if num_samples > 0 else 0.0
avg_rq = total_rq / num_samples if num_samples > 0 else 0.0

print(f"\n--> Validation complete. Displaying scores")
print(f"Evaluation Results:")
print(f"Mean IoU: {mIoU:.4f}")
print(f"Panoptic Quality (PQ): {avg_pq:.4f}")
print(f"Segmentation Quality (SQ): {avg_sq:.4f}")
print(f"Recognition Quality (RQ): {avg_rq:.4f}")

print(f"\n--> Visualizing sample prediction")
visualize_point_cloud(
    "Predicted Point Cloud", sample_data["points"], sample_data["semantic_pred"]
)
visualize_point_cloud(
    "Ground Truth Point Cloud", sample_data["points"], sample_data["semantic_gt"]
)
