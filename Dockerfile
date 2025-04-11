# Development Dockerfile
FROM ubuntu
SHELL ["/bin/bash", "-c"]
RUN groupadd --gid 1024 shared
RUN useradd -m --group sudo,shared scrapy && passwd -d scrapy

RUN apt-get update && \
	apt -y install sudo git nano curl gnupg build-essential python3 python3-dev python3-venv postgresql && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    gnupg \
    unzip \
    fonts-liberation \
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
    xdg-utils && \
    # Add Chrome repo using modern keyring approach
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update -y && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*


USER scrapy
WORKDIR /home/scrapy/
ENV VIRTUAL_ENV=/home/scrapy/.venv/scrapy
RUN mkdir .venv && python3 -m venv $VIRTUAL_ENV
ENV PATH=/home/scrapy/.venv/scrapy/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN echo "source ~/.venv/scrapy/bin/activate" >> ~/.bashrc
COPY requirements.txt /tmp/requirements.txt
RUN pip install setuptools
RUN pip install -r /tmp/requirements.txt

# RUN sudo /etc/init.d/postgresql start && \
# 	sudo -u postgres createuser mucho && sudo -u postgres createdb mucho && \
# 	echo "grant all privileges on database mucho to mucho; grant postgres to mucho;" | sudo -u postgres psql

WORKDIR /home/scrapy/work
RUN sudo chown :1024 . && sudo chmod 775 . && sudo chmod g+s .

#EXPOSE 8000/tcp
# CMD sudo service postgresql start && bash --init-file <(echo ". \"$HOME/.bashrc\"; make run")