import numpy as np

# Official SemanticKITTI label colors (index = class ID)
SEMANTIC_KITTI_COLORS = (
    np.array(
        [
            [0, 0, 0],  # 0 unlabeled
            [245, 150, 100],  # 1 car
            [245, 230, 100],  # 2 bicycle
            [150, 60, 30],  # 3 motorcycle
            [180, 30, 80],  # 4 truck
            [255, 0, 0],  # 5 other-vehicle
            [30, 30, 255],  # 6 person
            [200, 40, 255],  # 7 bicyclist
            [90, 30, 150],  # 8 motorcyclist
            [255, 0, 255],  # 9 road
            [255, 150, 255],  # 10 parking
            [75, 0, 75],  # 11 sidewalk
            [75, 0, 175],  # 12 other-ground
            [0, 200, 255],  # 13 building
            [50, 120, 255],  # 14 fence
            [0, 175, 0],  # 15 vegetation
            [0, 60, 135],  # 16 trunk
            [80, 240, 150],  # 17 terrain
            [150, 240, 255],  # 18 pole
            [0, 0, 255],  # 19 traffic sign
        ]
    )
    / 255.0
)  # normalize to [0, 1]

SEMANTIC_KITTI_ID_TO_INDEX = {
    0: 0,  # unlabeled
    10: 1,  # car
    11: 2,  # bicycle
    15: 3,  # motorcycle
    18: 4,  # truck
    20: 5,  # other-vehicle
    30: 6,  # person
    31: 7,  # bicyclist
    32: 8,  # motorcyclist
    40: 9,  # road
    44: 10,  # parking
    48: 11,  # sidewalk
    49: 12,  # other-ground
    50: 13,  # building
    51: 14,  # fence
    70: 15,  # vegetation
    71: 16,  # trunk
    72: 17,  # terrain
    80: 18,  # pole
    81: 19,  # traffic sign
}

DATASET_DIR = "./data/SemanticKITTI"
PREPROCESSED_DIR = "./preprocessed/SemanticKITTI"
SAVED_MODELS_DIR = "./saved_models"

TRAIN_SEQUENCES = ["00", "01", "02", "03", "04", "05", "06", "07", "09", "10"]
VAL_SEQUENCES = ["08"]
TEST_SEQUENCES = [
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21"
]
