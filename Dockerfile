# Debian Bookworm + Python 3.11 (ARM build on Pi 5)
FROM python:3.11-bookworm

# Basic tools needed to add the Raspberry Pi apt repo
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gnupg && \
    rm -rf /var/lib/apt/lists/*

# Add Raspberry Pi apt repo (this is where python3-lgpio lives)
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://archive.raspberrypi.com/debian/raspberrypi.gpg.key \
        | gpg --dearmor \
        | tee /etc/apt/keyrings/raspberrypi-archive-keyring.gpg > /dev/null && \
    echo "deb [signed-by=/etc/apt/keyrings/raspberrypi-archive-keyring.gpg arch=$(dpkg --print-architecture)] http://archive.raspberrypi.com/debian bookworm main" \
        > /etc/apt/sources.list.d/raspi.list

# Now install GPIO-related packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
         python3-lgpio python3-pigpio python3-rpi.gpio python3-gpiozero && \
    rm -rf /var/lib/apt/lists/*

# Create Working Directory
WORKDIR /app

#Install requirements
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

#Copy program
COPY pylcdmonitor.py /app
COPY font5x8.bin /app

#Execute
CMD ["python3", "pylcdmonitor.py"]
