#!/bin/bash

git config --global user.email "nizamphoenix@gmail.com"
git config --global user.name "nizamphoenix"
pip install kaggle
mkdir -p /home/ubuntu/.kaggle
## do vim  /home/ubuntu/.kaggle/kaggle.json and copy kaggle api creds that's downloaded from kaggle 
chmod 600 /home/ubuntu/.kaggle/kaggle.json
cd /home/ubuntu/kaggle-sartorius/data/raw/
kaggle competitions download -c sartorius-cell-instance-segmentation
unzip ./sartorius-cell-instance-segmentation.zip

mkdir -p /home/ubuntu/kaggle-sartorius/data/raw/cocopre
cd /home/ubuntu/kaggle-sartorius/data/raw/cocopre
kaggle datasets download -d mikeskim/cocopre
unzip cocopre.zip

mkdir -p /home/ubuntu/kaggle-sartorius/data/raw/sartorius-train-tif
cd /home/ubuntu/kaggle-sartorius/data/raw/sartorius-train-tif/
kaggle datasets download -d ks2019/sartorius-train-tif
unzip sartorius-train-tif

cd /home/ubuntu/kaggle-sartorius
