#!/bin/bash

set -e
DATESTR=$(date +%Y%m%d)
SCRIPT_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
# FIXME Change to correct image name
IMAGE_NAME=project

cd $SCRIPT_DIR/../..

docker build . -f containers/base/Dockerfile -t $IMAGE_NAME:$DATESTR -t $IMAGE_NAME:dev
docker push $IMAGE_NAME:$DATESTR
docker push $IMAGE_NAME:dev
