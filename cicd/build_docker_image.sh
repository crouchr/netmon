#!/bin/bash
cd ..
docker build --no-cache -t cicd:netmon .
docker tag cicd:netmon registry:5000/netmon:$VERSION
docker push registry:5000/netmon:$VERSION
docker rmi cicd:netmon

