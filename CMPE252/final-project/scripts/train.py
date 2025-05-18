import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm

from src.models.simplemodel import SimpleModel
from src.datasets.semantickitti_dataset import SemanticKITTIDataset
from src.constants import PREPROCESSED_DIR, TRAIN_SEQUENCES, SAVED_MODELS_DIR
from src.utils.train import collate_fn, discriminative_loss

BATCH_SIZE = 4
NUM_EPOCHS = 10
LEARNING_RATE = 0.001
INSTANCE_EMBEDDING_DIM = 32
SAVE_INTERVAL = 1

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"--> Using device: {device}")

# Loading dataset
dataset = SemanticKITTIDataset(PREPROCESSED_DIR, TRAIN_SEQUENCES)
dataloader = DataLoader(
    dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=4, collate_fn=collate_fn
)

print("\n--> Dataset loaded")

# Loading model
model = SimpleModel(instance_embedding_dim=INSTANCE_EMBEDDING_DIM)
print("\n--> SimpleModel loaded")

# Training
print("\n--> Begin training")

model.to(device)
model.train()

semantic_criterion = nn.CrossEntropyLoss(ignore_index=0)  # Ignore background class
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

model_folder = os.path.join(PREPROCESSED_DIR, "simplemodel")
checkpoint_folder = os.path.join(model_folder, "checkpoints")
os.makedirs(checkpoint_folder, exist_ok=True)

for epoch in range(NUM_EPOCHS):

    epoch_semantic_loss = 0.0
    epoch_disc_loss = 0.0
    num_batches = 0

    progress_bar = tqdm(
        dataloader, desc=f"Epoch {epoch+1}/{NUM_EPOCHS}: SL = 0.0000, DL = 0.0000"
    )
    for batch in progress_bar:
        points = batch["points"].to(device)  # [batch_size, max_points, 4]
        semantic_labels = batch["semantic_labels"].to(
            device
        )  # [batch_size, max_points]
        instance_labels = batch["instance_labels"].to(
            device
        )  # [batch_size, max_points]
        masks = batch["masks"].to(device)  # [batch_size, max_points]

        # Fix invalid labels (map 19 to 0)
        semantic_labels[semantic_labels == 19] = 0

        # Forward pass
        optimizer.zero_grad()
        semantic_pred, instance_pred = model(
            points
        )  # [batch_size * max_points, 19], [batch_size * max_points, 16]

        # Semantic loss
        semantic_loss = semantic_criterion(
            semantic_pred.view(-1, 19), semantic_labels.view(-1)
        )

        # Discriminative loss
        instance_pred = instance_pred.view(
            points.size(0), points.size(1), -1
        )  # [batch_size, max_points, 16]
        disc_loss = discriminative_loss(instance_pred, instance_labels, masks=masks)

        # Total loss
        total_loss = semantic_loss + disc_loss
        total_loss.backward()
        optimizer.step()

        # Accumulate losses
        epoch_semantic_loss += semantic_loss.item()
        epoch_disc_loss += disc_loss.item()
        num_batches += 1

        # Update progress bar with current average losses
        avg_semantic_loss = epoch_semantic_loss / num_batches
        avg_disc_loss = epoch_disc_loss / num_batches
        progress_bar.set_description(
            f"Epoch {epoch+1}/{NUM_EPOCHS}: SL = {avg_semantic_loss:.4f}, DL = {avg_disc_loss:.4f}"
        )

    # Save checkpoint at the end of each epoch
    checkpoint_path = os.path.join(checkpoint_folder, f"checkpoint_epoch_{epoch+1}.pth")
    torch.save(
        {
            "epoch": epoch + 1,
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "semantic_loss": avg_semantic_loss,
            "discriminative_loss": avg_disc_loss,
        },
        checkpoint_path,
    )
    print(f"Saved checkpoint: {checkpoint_path}")

# Save final model
simplemodel_path = os.path.join(model_folder, "simplemodel.pth")
torch.save(model.state_dict(), simplemodel_path)
print(f"Saved final model: {simplemodel_path}")
