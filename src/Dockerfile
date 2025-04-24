# Use an official Python runtime as a parent image
FROM python:3.11-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# install chromium
RUN playwright install --with-deps --only-shell chromium

# docker run -it --rm --ipc=host capbotimage /bin/bash
