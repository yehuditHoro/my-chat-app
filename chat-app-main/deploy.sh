#!/bin/bash
version=$1
# git_version="v${version}"
img_name_and_tag="chat_img:${version}"
IMAGE_EXISTS=$(docker images | grep $img_name_and_tag)

if docker image inspect ${img_name_and_tag} > /dev/null 2>&1; then
   echo "The image $img_name_and_tag already exist, do you want to rebuild it (Y/N)"
   read -r rebuild_image
    if [[ "$rebuild_image" == "Y" ]]; then
       # Delete the existing image
       echo "Deleting the existing image..."
       docker image rm ${img_name_and_tag}
       # Build the image
       echo "Building the image..."
       docker build -t ${img_name_and_tag} .
    else
     # Use the existing image
       echo "Using the existing image..."
    fi
else
     echo "Build the image"
     docker build -t ${img_name_and_tag} .
fi

# if [ -n "$2" ]; then
#    commit_hash=$2
#    docker volume create chat-data
#    git tag v${version} ${commit_hash} 
#    git push origin v${version}
# fi

echo "Do you want to push to GCR? (Y/N)"
read -r push_to_gcp
if [[ "$push_to_gcp" == "Y" ]]; then
     gcloud config set auth/impersonate_service_account artifact-admin-sa@grunitech-mid-project.iam.gserviceaccount.com
     # gcloud auth application-default login --impersonate-service-account artifact-admin-sa@grunitech-mid-project.iam.gserviceaccount.com
     gcloud auth configure-docker me-west1-docker.pkg.dev
     docker tag ${img_name_and_tag} me-west1-docker.pkg.dev/grunitech-mid-project/yehudit-chat-app-images/chat-app:${version}
     docker push me-west1-docker.pkg.dev/grunitech-mid-project/yehudit-chat-app-images/chat-app:${version}
     gcloud config unset auth/impersonate_service_account
fi