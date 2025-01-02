# Use the official Python image from the Docker Hub
FROM python:3.12-slim AS builder

# Set working directory
WORKDIR /app

# Copy only the requirements file
COPY requirements.txt .

# Install build dependencies and create virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Start a new stage
FROM python:3.12-slim
LABEL org.opencontainers.image.source=https://github.com/MrStarkEG1/zone-h-scraper
LABEL org.opencontainers.image.description="zone-h-scraper"

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set working directory
WORKDIR /app

# Install Xvfb and other necessary dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libxshmfence1 \
    libgbm1 \
    libasound2 \
    xvfb && \
    rm -rf /var/lib/apt/lists/* && \
    /opt/venv/bin/playwright install chromium && \
    /opt/venv/bin/playwright install-deps


COPY .env .

# Copy application code
COPY . .

# Set PATH to use virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# # Create a script to run Xvfb and the application
# RUN echo '#!/bin/bash\n python ./zoneh/main.py' > /app/start.sh && \
#     chmod +x /app/start.sh

# # Command to run the script
# CMD ["/app/start.sh"]

CMD ["python", "./zoneh/main.py"]