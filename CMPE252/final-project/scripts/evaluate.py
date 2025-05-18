import os
import torch
import numpy as np
import open3d as o3d
from torch.utils.data import DataLoader
from sklearn.cluster import DBSCAN
from scipy.optimize import linear_sum_assignment

from src.datasets import semantickitti_dataset
from src.models import SimpleModel
from src.utils import compute_iou, collate_fn
from src.constants import (
    SEMANTIC_KITTI_COLORS,
    SEMANTIC_KITTI_ID_TO_INDEX,
    DATASET_DIR,
    SAVED_MODELS_DIR,
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"--> Using device: {device}")

print("\n--> Preparing validation dataset")
val_sequence = ["08"]
val_files = []
for seq in val_sequence:
    seq_path = os.path.join(DATASET_DIR, "sequences", seq, "velodyne")
    scans = sorted(os.listdir(seq_path))
    val_files.extend(
        [
            (
                os.path.join(seq_path, scan),
                os.path.join(seq_path, "../labels", scan.replace(".bin", ".label")),
            )
            for scan in scans
        ]
    )

val_dataset = semantickitti_dataset(val_files, augment=False)
val_loader = DataLoader(
    val_dataset,
    batch_size=4,
    shuffle=False,
    collate_fn=collate_fn,
    num_workers=8,
    pin_memory=True,
)


# Function to compute instance AP
def compute_instance_ap(pred_clusters, gt_instances):
    pred_clusters = pred_clusters.astype(np.int32)
    gt_instances = gt_instances.astype(np.int32)
    unique_pred = np.unique(pred_clusters[pred_clusters != -1])
    unique_gt = np.unique(gt_instances[gt_instances != 0])

    if len(unique_pred) == 0 or len(unique_gt) == 0:
        return 0.0

    # Compute IoU between predicted and ground truth instances
    iou_matrix = np.zeros((len(unique_pred), len(unique_gt)))
    for i, pred_id in enumerate(unique_pred):
        for j, gt_id in enumerate(unique_gt):
            pred_mask = pred_clusters == pred_id
            gt_mask = gt_instances == gt_id
            intersection = np.sum(pred_mask & gt_mask)
            union = np.sum(pred_mask | gt_mask)
            iou_matrix[i, j] = intersection / union if union > 0 else 0.0

    # Hungarian matching
    row_ind, col_ind = linear_sum_assignment(-iou_matrix)

    # Compute AP
    ious = iou_matrix[row_ind, col_ind]
    ap = np.mean(ious > 0.5)  # Threshold IoU > 0.5 for a true positive
    return ap


# Lists to store metrics and sample data
iou_scores = []
pixel_acc_scores = []
instance_ap_scores = []
sample_data = []

print("\n--> Evaluating model")
model = SimpleModel(instance_embedding_dim=32).to(device)
model.load_state_dict(torch.load(SAVED_MODELS_DIR))
model.eval()
print(f"Loaded saved model from {SAVED_MODELS_DIR}")

for batch_idx, batch in enumerate(val_loader):
    for sample_idx, (points, semantic_labels, instance_labels) in enumerate(batch):
        points = points.unsqueeze(0).to(device)
        semantic_labels = semantic_labels.to(device)
        instance_labels = instance_labels.to(device)

        # Model prediction
        with torch.no_grad():
            semantic_pred, instance_pred = model(points)
            pred_labels = torch.argmax(semantic_pred, dim=2).squeeze(0)

        # Semantic evaluation
        pred_labels_np = pred_labels.cpu().numpy()
        semantic_labels_np = semantic_labels.cpu().numpy()
        iou = compute_iou(pred_labels_np, semantic_labels_np)
        iou_scores.append(iou)

        correct = (pred_labels == semantic_labels).sum().item()
        total = semantic_labels.numel()
        pixel_acc = correct / total
        pixel_acc_scores.append(pixel_acc)

        # Instance evaluation
        instance_pred_np = instance_pred.squeeze(0).cpu().numpy()  # [N, 32]
        instance_labels_np = instance_labels.cpu().numpy()  # [N]

        # Cluster instance embeddings using DBSCAN
        dbscan = DBSCAN(eps=0.5, min_samples=10, metric="euclidean")
        pred_clusters = dbscan.fit_predict(instance_pred_np)

        # Compute instance AP
        instance_ap = compute_instance_ap(pred_clusters, instance_labels_np)
        instance_ap_scores.append(instance_ap)

        # Store sample data for visualization
        sample_data.append(
            {
                "points": points.squeeze(0).cpu().numpy(),  # [N, 4]
                "pred_labels": pred_labels_np,  # [N]
                "pred_clusters": pred_clusters,  # [N]
                "batch_idx": batch_idx,
                "sample_idx": sample_idx,
                "pixel_acc": pixel_acc,
                "instance_ap": instance_ap,
            }
        )

# Compute semantic metrics
iou_array = np.array(iou_scores)
highest_iou = iou_array.max()
mean_iou = iou_array.mean()
lowest_iou = iou_array.min()

pixel_acc_array = np.array(pixel_acc_scores)
highest_pixel_acc = pixel_acc_array.max()
mean_pixel_acc = pixel_acc_array.mean()
lowest_pixel_acc = pixel_acc_array.min()

# Compute instance metrics
instance_ap_array = np.array(instance_ap_scores)
highest_instance_ap = instance_ap_array.max()
mean_instance_ap = instance_ap_array.mean()
lowest_instance_ap = instance_ap_array.min()

# Find the index of the sample with the highest pixel accuracy
highest_acc_idx = np.argmax(pixel_acc_array)

print("\n--> Semantic IoU Scores:")
print(f"  Highest IoU: {highest_iou:.4f}")
print(f"  Mean IoU: {mean_iou:.4f}")
print(f"  Lowest IoU: {lowest_iou:.4f}")

print("\n--> Semantic Pixel Accuracy Scores:")
print(f"  Highest Pixel Accuracy: {highest_pixel_acc:.4f}")
print(f"  Mean Pixel Accuracy: {mean_pixel_acc:.4f}")
print(f"  Lowest Pixel Accuracy: {lowest_pixel_acc:.4f}")

print("\n--> Instance AP Scores:")
print(f"  Highest Instance AP: {highest_instance_ap:.4f}")
print(f"  Mean Instance AP: {mean_instance_ap:.4f}")
print(f"  Lowest Instance AP: {lowest_instance_ap:.4f}")

print("\n--> Rendering prediction for sample with highest pixel accuracy")
best_sample = sample_data[highest_acc_idx]
points = best_sample["points"][:, :3]  # [N, 3]
pred_labels = best_sample["pred_labels"]  # [N]
pred_clusters = best_sample["pred_clusters"]  # [N]
batch_idx = best_sample["batch_idx"]
sample_idx = best_sample["sample_idx"]
print(
    f"Visualizing Batch {batch_idx}, Sample {sample_idx} "
    f"(Pixel Accuracy: {best_sample['pixel_acc']:.4f}, Instance AP: {best_sample['instance_ap']:.4f})"
)

# Map predicted class indices to SemanticKITTI label IDs
index_to_id = {v: k for k, v in SEMANTIC_KITTI_ID_TO_INDEX.items()}
pred_label_ids = np.array([index_to_id.get(label, 0) for label in pred_labels])

# Map label IDs to color indices
color_indices = np.vectorize(SEMANTIC_KITTI_ID_TO_INDEX.get)(pred_label_ids, 0)

# Get semantic colors
semantic_colors = SEMANTIC_KITTI_COLORS[color_indices]  # [N, 3]

# Create instance colors (random colors for each cluster)
unique_clusters = np.unique(pred_clusters[pred_clusters != -1])
instance_colors = np.zeros_like(semantic_colors)
np.random.seed(42)
cluster_colors = np.random.rand(len(unique_clusters), 3)
for i, cluster_id in enumerate(unique_clusters):
    instance_colors[pred_clusters == cluster_id] = cluster_colors[i]
instance_colors[pred_clusters == -1] = [0, 0, 0]  # Noise points in black

# Create point clouds
semantic_pcd = o3d.geometry.PointCloud()
semantic_pcd.points = o3d.utility.Vector3dVector(points)
semantic_pcd.colors = o3d.utility.Vector3dVector(semantic_colors)

instance_pcd = o3d.geometry.PointCloud()
instance_pcd.points = o3d.utility.Vector3dVector(points)
instance_pcd.colors = o3d.utility.Vector3dVector(instance_colors)

# Visualize both semantic and instance predictions
o3d.visualization.draw_geometries([semantic_pcd], window_name="Semantic Prediction")
o3d.visualization.draw_geometries([instance_pcd], window_name="Instance Prediction")
