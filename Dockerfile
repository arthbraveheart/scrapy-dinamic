# Development Dockerfile using Playwright base image
FROM mcr.microsoft.com/playwright:v1.49.1-noble

# System setup: Create user and install essential dependencies
RUN groupadd --gid 1024 shared && \
    useradd -m --group sudo,shared scrapy && passwd -d scrapy

# Install system dependencies (Postgres client, build tools, etc.)
RUN apt-get update && \
    apt-get install -y sudo git nano curl build-essential python3-venv postgresql-client libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Switch to non-root user and set up Python virtual environment
USER scrapy
WORKDIR /home/scrapy/
ENV VIRTUAL_ENV=/home/scrapy/.venv/scrapy
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="/home/scrapy/.venv/scrapy/bin:$PATH"
RUN echo "source ~/.venv/scrapy/bin/activate" >> ~/.bashrc

# Install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir setuptools wheel && \
    pip install --no-cache-dir -r /tmp/requirements.txt

# Configure work directory permissions
WORKDIR /home/scrapy/work
RUN sudo chown :1024 . && sudo chmod 775 . && sudo chmod g+s .