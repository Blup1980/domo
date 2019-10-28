# Pull base image
FROM balenalib/raspberrypi3-debian:buster
MAINTAINER Xavier Raemy

RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key | apt-key add -
RUN wget -q -O /etc/apt/sources.list.d/mosquitto-buster.list http://repo.mosquitto.org/debian/mosquitto-buster.list
RUN apt-get update && apt-get install -y mosquitto && rm -rf /var/lib/apt/lists/*

RUN adduser --system --disabled-password --disabled-login mosquitto

COPY config /mqtt/config
VOLUME ["/mqtt/config", "/mqtt/data", "/mqtt/log"]

EXPOSE 1883 9001
CMD /usr/sbin/mosquitto -c /mqtt/config/mosquitto.conf
