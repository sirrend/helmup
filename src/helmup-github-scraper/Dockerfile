# syntax=docker/dockerfile:1.2
# Use the base image for Python 3.12
FROM python:3.12-slim

# Set the working directory
WORKDIR /usr/src/app

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    gzip \
    git \
    openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Ensure known_hosts file is set up for GitHub
RUN mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

# Copy code
COPY src/ .

# Use the --mount=type=ssh option to securely forward SSH keys during the build process
RUN --mount=type=ssh pip install --no-cache-dir -r requirements.txt

# Set the CMD to your handler
CMD ["python", "main.py"]