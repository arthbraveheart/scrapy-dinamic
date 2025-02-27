# Development Dockerfile
FROM ubuntu
SHELL ["/bin/bash", "-c"]
RUN groupadd --gid 1024 shared
RUN useradd -m --group sudo,shared mucho && passwd -d mucho

RUN apt-get update && \
	apt -y install sudo git nano curl gnupg build-essential python3 python3-dev python3-venv postgresql


USER mucho
WORKDIR /home/mucho/
ENV VIRTUAL_ENV=/home/mucho/.venv/mucho
RUN mkdir .venv && python3 -m venv $VIRTUAL_ENV
ENV PATH=/home/mucho/.venv/mucho/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN echo "source ~/.venv/mucho/bin/activate" >> ~/.bashrc
COPY requirements.txt /tmp/requirements.txt
RUN pip install setuptools
RUN pip install -r /tmp/requirements.txt

# RUN sudo /etc/init.d/postgresql start && \
# 	sudo -u postgres createuser mucho && sudo -u postgres createdb mucho && \
# 	echo "grant all privileges on database mucho to mucho; grant postgres to mucho;" | sudo -u postgres psql

WORKDIR /home/mucho/work
RUN sudo chown :1024 . && sudo chmod 775 . && sudo chmod g+s .

EXPOSE 8000/tcp
# CMD sudo service postgresql start && bash --init-file <(echo ". \"$HOME/.bashrc\"; make run")