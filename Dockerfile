FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for MCP servers
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install MCP servers
RUN npm install -g \
    @modelcontextprotocol/server-filesystem \
    @modelcontextprotocol/server-git \
    @modelcontextprotocol/server-shell \
    @modelcontextprotocol/server-memory

# Copy application
COPY cynetics.py .
COPY cynetics.json .

# Create non-root user
RUN useradd -m -u 1000 cynetics && \
    mkdir -p workspace artifacts logs && \
    chown -R cynetics:cynetics /app

USER cynetics

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "cynetics.py"]
CMD ["--help"]
