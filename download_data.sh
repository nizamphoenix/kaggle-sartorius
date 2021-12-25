#!/bin/bash

chmod 600 /home/ubuntu/.kaggle/kaggle.json
cd kaggle-sartorius/data/raw
kaggle competitions download -c sartorius-cell-instance-segmentation
unzip ./sartorius-cell-instance-segmentation.zip

mkdir cocopre
cd ./cocopre/
kaggle datasets download -d mikeskim/cocopre
unzip cocopre.zip