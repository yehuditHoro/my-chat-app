#!/bin/bash
version='latest'
if [ $# -ne 0 ]; then
  # Arguments were passed, so use them
    version=$1
fi


docker volume create chat-app-data
docker build -t  chat-app:${version} .
docker run -v chat-app-data:/chatApp/data -p 5000:5000 --name chat-App-run chat-app:${version}