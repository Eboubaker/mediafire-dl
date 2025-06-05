FROM python:3.9-slim

WORKDIR /app

# Install Chrome
RUN apt-get update && apt-get install -y gnupg wget curl
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Install necessary system dependencies for SeleniumBase and Chrome
RUN apt-get update && apt-get install -y \
    xvfb \
    xorg \
    unzip \
    libgbm1 \
    python3-tk \
    python3-dev \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the ad_block extension
COPY downloaded_files/ad_block /root/.local/share/seleniumbase/extensions/chrome/ad_block

# Copy the application code
COPY mediafire_dl.py .
COPY setup.py .
COPY LICENSE .
COPY README.md .

# Install the package
RUN pip install -e .

# Create a directory for downloaded files
RUN mkdir -p /downloads

# Set the working directory for downloads
VOLUME /downloads
WORKDIR /downloads

# Set up display for Selenium
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1
ENV CHROME_PATH=/usr/bin/google-chrome-stable

# Create an entrypoint script
RUN echo '#!/bin/bash\nXvfb :99 -screen 0 1280x800x24 -ac &\nexec mediafire-dl "$@"' > /entrypoint.sh && \
    chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]