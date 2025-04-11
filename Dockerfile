# Development Dockerfile
FROM ubuntu:24.04
SHELL ["/bin/bash", "-c"]
RUN groupadd --gid 1024 shared
RUN useradd -m --group sudo,shared scrapy && passwd -d scrapy

# System dependencies with required libraries
RUN apt-get update && \
    apt-get install -y sudo git nano curl gnupg build-essential python3 python3-dev python3-venv postgresql && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg \
    unzip \
    fonts-liberation \
    # Core dependencies
    libasound2t64 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    # Additional Playwright dependencies
    libopus0 \
    libwoff1 \
    libharfbuzz-icu0 \
    libgstreamer-plugins-base1.0-0 \
    libgstreamer1.0-0 \
    libgstreamer-gl1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    libopenjp2-7 \
    libwebpdemux2 \
    libwebp7 \
    libenchant-2-2 \
    libsecret-1-0 \
    libhyphen0 \
    libmanette-0.2-0 \
    libatomic1 \
    libevent-2.1-7 \
    libvpx9 \
    libnotify4 \
    libxslt1.1 \
    libegl1 \
    libgles2 \
    libgl1 \
    libflite1 \
    libepoxy0 \
    libwayland-client0 \
    libwayland-egl1 \
    libwayland-server0 \
    libxml2 \
    libavif16 \
    libwebpmux3 && \
    # Clean up
    rm -rf /var/lib/apt/lists/*

USER scrapy
WORKDIR /home/scrapy/
ENV VIRTUAL_ENV=/home/scrapy/.venv/scrapy
RUN mkdir -p .venv && python3 -m venv $VIRTUAL_ENV
ENV PATH=/home/scrapy/.venv/scrapy/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN echo "source ~/.venv/scrapy/bin/activate" >> ~/.bashrc

COPY requirements.txt /tmp/requirements.txt
RUN pip install setuptools wheel && \
    pip install -r /tmp/requirements.txt && \
    playwright install --with-deps

WORKDIR /home/scrapy/work
RUN sudo chown :1024 . && sudo chmod 775 . && sudo chmod g+s .