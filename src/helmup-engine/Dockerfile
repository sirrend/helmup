# syntax=docker/dockerfile:1.2
# Use the base image for Python 3.12
FROM python:3.12-slim

# Set the working directory
WORKDIR /usr/src

# Install necessary packages
RUN apt-get update && apt-get install -y \
    wget \
    tar \
    gzip \
    git \
    curl \ 
    openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Download and install Pluto
# Download and install Pluto based on architecture
ARG TARGETARCH
RUN case "$TARGETARCH" in \
        amd64) PLUTO_URL=https://github.com/FairwindsOps/pluto/releases/download/v5.18.6/pluto_5.18.6_linux_amd64.tar.gz ;; \
        arm64) PLUTO_URL=https://github.com/FairwindsOps/pluto/releases/download/v5.18.6/pluto_5.18.6_linux_arm64.tar.gz ;; \
        *) echo "unsupported architecture: $TARGETARCH" && exit 1 ;; \
    esac && \
    wget $PLUTO_URL && \
    tar -zxvf $(basename $PLUTO_URL) -C /usr/local/bin/ && \
    chmod +x /usr/local/bin/pluto && \
    rm $(basename $PLUTO_URL)

# Install Helm
ENV VERIFY_CHECKSUM=false
RUN curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Ensure known_hosts file is set up for GitHub
RUN mkdir -p /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts

# Copy code
COPY src/ .

# Use the --mount=type=ssh option to securely forward SSH keys during the build process
RUN --mount=type=ssh pip install --no-cache-dir -r requirements.txt

# Set the CMD to your handler
CMD ["python", "api.py"]