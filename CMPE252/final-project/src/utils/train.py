import torch
import torch.nn.functional as F


def collate_fn(batch):
    # Determine max number of points in this batch
    max_points = max([item["points"].shape[0] for item in batch])
    batch_size = len(batch)

    # Initialize tensors with padding
    points_batch = torch.zeros(
        batch_size, max_points, 4, device=batch[0]["points"].device
    )
    semantic_labels_batch = torch.zeros(
        batch_size,
        max_points,
        dtype=torch.long,
        device=batch[0]["semantic_labels"].device,
    )
    instance_labels_batch = torch.zeros(
        batch_size,
        max_points,
        dtype=torch.long,
        device=batch[0]["instance_labels"].device,
    )
    masks = torch.zeros(
        batch_size, max_points, dtype=torch.bool, device=batch[0]["points"].device
    )

    # Fill tensors with data
    for i, item in enumerate(batch):
        n_points = item["points"].shape[0]
        points_batch[i, :n_points] = item["points"]
        semantic_labels_batch[i, :n_points] = item["semantic_labels"]
        instance_labels_batch[i, :n_points] = item["instance_labels"]
        masks[i, :n_points] = True

    return {
        "points": points_batch,
        "semantic_labels": semantic_labels_batch,
        "instance_labels": instance_labels_batch,
        "masks": masks,
    }


def discriminative_loss(
    embeddings, instance_ids, masks=None, delta_v=0.5, delta_d=1.5, l_reg=0.001
):
    batch_size = embeddings.shape[0]

    # If no masks provided, assume all points are valid
    if masks is None:
        masks = torch.ones_like(instance_ids, dtype=torch.bool)

    loss_var, loss_dist, loss_reg = 0.0, 0.0, 0.0

    for b in range(batch_size):
        # Only consider valid points from the mask
        valid_mask = masks[b]
        embedding = embeddings[b][valid_mask]
        instance = instance_ids[b][valid_mask]

        unique_instances = torch.unique(
            instance[instance != 0]
        )  # Ignore background (0)

        # Variance loss
        var_loss = 0.0
        for inst in unique_instances:
            mask = instance == inst
            if mask.sum() > 1:
                mean_embedding = embedding[mask].mean(dim=0)
                var = torch.norm(embedding[mask] - mean_embedding, dim=1)
                var = torch.clamp(var - delta_v, min=0) ** 2
                var_loss += var.mean()

        if len(unique_instances) > 0:
            loss_var += var_loss / len(unique_instances)

        # Distance loss
        dist_loss = 0.0
        if len(unique_instances) > 1:
            means = []
            for inst in unique_instances:
                inst_mask = instance == inst
                if inst_mask.sum() > 0:  # Ensure we have points for this instance
                    means.append(embedding[inst_mask].mean(dim=0))

            if len(means) > 1:
                means = torch.stack(means)
                for i in range(len(means)):
                    for j in range(i + 1, len(means)):
                        dist = torch.norm(means[i] - means[j])
                        dist_loss += torch.clamp(delta_d - dist, min=0) ** 2
                dist_loss /= len(means) * (len(means) - 1) / 2

        loss_dist += dist_loss

        # Regularization
        if valid_mask.sum() > 0:
            loss_reg += torch.norm(embedding, dim=1).mean()

    loss_var /= batch_size
    loss_dist /= batch_size
    loss_reg = l_reg * (loss_reg / batch_size)

    return loss_var + loss_dist + loss_reg
