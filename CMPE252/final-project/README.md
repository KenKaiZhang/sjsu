# CSE 252 Final Project

**_This repository contains the code for CSE 252's final project._**

## Overview

The goal of this project is to expand my understanding about the tools and technologies being leveraged in the field of object detection. In this project, we focus on **panoptic segmentation**, a concept developed in 2019 that suggests a more streamlined and optimized way to train models that are capable of both semantic and object detection. This project is divided into 3 main components :

1. Visualizing Dataset
2. Utilizing Dataset
3. Model

The target dataset of this project is [SEMANTIC KITTI](https://semantic-kitti.org/dataset.html), a popular LiDAR based dataset that contains semantic and instance annotation for all its point cloud data.

## Setup

**Hardware Requirements** : NVIDIA GPU is preferred

**Software Requirements** : 

- VSCode
- Docker
- Python 3.11+
- PyTorch 2.2.2
- CUDA 11.8.0

1. Download [SEMANTIC KITTI](https://semantic-kitti.org/dataset.html).'

2. In the `docker-compose.yaml` file, mount the dataset to the docker container so it can access the dataset freely withou have to duplicate all 80GB of it. 

3. Open VSCode and install **Dev Containers**. On the bottom left of the screen, click on the `><` icon and select **Reopen in Container** (this can also be from a popup). 
    - This should build the container and link VSCode to the container

4. Run `pip install -r requirements.txt`

## Visualizing Datasets

**scripts/dataset_reading.py** : gives an overview of the structure of Semantic KITTI and renders an example

**scripts/segmentation.py** : simple segmentations techniques doable on the dataset without model training (with renders)

## Utilizing Datasets 

**scripts/preprocessing.py** : preprocesses the dataset for model traing and testing

- voxelization
- augmentations
- noise
- normalization

## Model

Run scripts in this order :

1. **preprocessing.py**
2. **train.py**
3. **evaluate.py**

This will preprocess the data, train _SimpleModel_, and evaluate _SimpleModel_ performace. 

If there are other models you would like to test, simply add them to **src/models** and change which model is being trained in **scripts/train.py**

