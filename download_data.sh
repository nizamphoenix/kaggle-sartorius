#!/bin/bash

pip install kaggle
chmod 600 /home/ubuntu/.kaggle/kaggle.json
cd kaggle-sartorius/data/raw
kaggle competitions download -c sartorius-cell-instance-segmentation
unzip ./sartorius-cell-instance-segmentation.zip

mkdir cocopre
cd ./cocopre/
kaggle datasets download -d mikeskim/cocopre
unzip cocopre.zip

mkdir sartorius-train-tif
cd ./sartorius-train-tif/
kaggle datasets download -d ks2019/sartorius-train-tif
unzip sartorius-train-tif
