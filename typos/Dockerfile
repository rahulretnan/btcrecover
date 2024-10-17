# Use official Python 3.12 image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install binutils and Tcl/Tk libraries
RUN apt-get update && apt-get install -y \
    binutils \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyInstaller
RUN pip install --no-cache-dir pyinstaller

# The executable will be created when the container runs
