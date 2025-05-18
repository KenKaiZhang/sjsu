import torch.nn as nn


class SimpleModel(nn.Module):
    def __init__(self, instance_embedding_dim=32):
        super(SimpleModel, self).__init__()
        # Shared backbone
        self.fc1 = nn.Linear(4, 64)
        self.fc2 = nn.Linear(64, 128)

        self.fc3_semantic = nn.Linear(128, 19)
        self.fc3_instance = nn.Linear(128, instance_embedding_dim)

        self.relu = nn.ReLU()

    def forward(self, points):

        x = self.relu(self.fc1(points))
        x = self.relu(self.fc2(x))

        semantic_pred = self.fc3_semantic(x)
        instance_pred = self.fc3_instance(x)

        return semantic_pred, instance_pred
