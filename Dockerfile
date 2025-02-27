# Development Dockerfile
FROM ubuntu
SHELL ["/bin/bash", "-c"]
RUN groupadd --gid 1024 shared
RUN useradd -m --group sudo,shared scrapy && passwd -d scrapy

RUN apt-get update && \
	apt -y install sudo git nano curl gnupg build-essential python3 python3-dev python3-venv postgresql


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