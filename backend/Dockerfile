FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for mysqlclient and dos2unix
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Convert line endings and make entrypoint executable
RUN dos2unix entrypoint.sh && \
    chmod +x entrypoint.sh

EXPOSE 8001

CMD ["/bin/bash", "-c", "exec ./entrypoint.sh"]