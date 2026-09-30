FROM python:3.11-slim

# Install system utilities, Java (required by ZAP), and curl/wget
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Create reports directory
RUN mkdir -p reports

# Default command placeholder (will be overridden in CI or run script)
CMD ["python", "zap_local_test.py"]