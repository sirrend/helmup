#!/bin/bash

# Assigning arguments to variables
DOCKERHUB_USERNAME="sirrend"
IMAGE_NAME="helmup-github-scraper"
IMAGE_TAG="0.1.4"

# Log in to Docker Hub
echo "Logging in to Docker Hub..."
cat ~/.docker-sirrend-password | docker login -u business@sirrend.com --password-stdin

# Check if login was successful
if [ $? -ne 0 ]; then
    echo "Docker login failed. Please check your username and password."
    exit 1
fi

# Add the id_rsa key to the known hosts
ssh-add ~/.ssh/id_rsa

# Create and use a new buildx builder instance
echo "Setting up Docker buildx builder..."
docker buildx create --use

# Build the Docker image for both amd64 and arm64 architectures
echo "Building Docker images for amd64 and arm64..."
export DOCKER_BUILDKIT=1
docker buildx build --platform linux/amd64,linux/arm64 -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} --ssh default --push .

# Check if push was successful
if [ $? -ne 0 ]; then
    echo "Docker push failed. Please check the image name and tag."
    exit 1
fi

# Log out from Docker Hub
echo "Logging out from Docker Hub..."
docker logout

echo "Image $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG pushed successfully."

helm upgrade --install $IMAGE_NAME chart/