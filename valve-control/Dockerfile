# Pull base image
FROM resin/rpi-raspbian:jessie
MAINTAINER Xavier Raemy <xavier.raemy@gmail.com>

RUN apt-get update && apt-get install -y git python3 python3-setuptools python3-smbus python3-gi less && rm -rf /var/lib/apt/lists/*
RUN git clone https://github.com/eclipse/paho.mqtt.python && cd paho.mqtt.python && python3 setup.py install

RUN adduser --system --disabled-password --disabled-login valve

#COPY src /valve/src

RUN mkdir -p /valve/src
run mkdir -p /valve/log

CMD python3 /valve/src/run.py

