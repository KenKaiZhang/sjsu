FROM nvidia/cuda:11.8.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility
ENV PYTHONPATH=/workspace/src

# Install dependencies and Python 3.12
RUN apt-get update && apt-get install -y \
    software-properties-common curl gnupg2 \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.12 python3.12-dev python3.12-venv \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y libgl1
RUN apt-get update && apt-get install -y libgomp1
RUN apt-get update && apt-get install -y wget


# Create and activate a virtual environment
RUN python3.12 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install pip in the virtual environment
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12

# Set python3 and python to point to Python 3.12
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    ln -sf /usr/bin/python3 /usr/bin/python

# Upgrade pip in the virtual environment
RUN pip install --upgrade pip

# Install PyTorch (adjust CUDA version as needed)
RUN pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2

# Set working directory
WORKDIR /workspace

CMD ["/bin/bash"]