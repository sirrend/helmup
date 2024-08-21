#!/bin/bash

# Assigning arguments to variables
DOCKERHUB_USERNAME="sirrend"
IMAGE_NAME="helmup-notifications-service"
IMAGE_TAG="0.1.3"

# Log in to Docker Hub
echo "Logging in to Docker Hub..."
cat ~/.docker-sirrend-password | docker login -u business@sirrend.com --password-stdin

# Check if login was successful
if [ $? -ne 0 ]; then
    echo "Docker login failed. Please check your username and password."
    exit 1
fi

# Create and use a new buildx builder instance
echo "Setting up Docker buildx builder..."
docker buildx create --use

# Build the Docker image for both amd64 and arm64 architectures
echo "Building Docker images for amd64 and arm64..."
docker buildx build --platform linux/amd64,linux/arm64 -t ${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${IMAGE_TAG} --push .

# Check if push was successful
if [ $? -ne 0 ]; then
    echo "Docker push failed. Please check the image name and tag."
    exit 1
fi

# Log out from Docker Hub
echo "Logging out from Docker Hub..."
docker logout

echo "Image $DOCKERHUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG pushed successfully."
