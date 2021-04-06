#!/bin/bash
cd ..
docker build --no-cache -t cicd:netmond .
docker tag cicd:netmond registry:5000/netmond:$VERSION
docker push registry:5000/netmond:$VERSION
docker rmi cicd:netmond

