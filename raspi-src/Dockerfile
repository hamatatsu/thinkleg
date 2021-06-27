# syntax=docker/dockerfile:1

FROM python:3.7.5

WORKDIR /raspi-src

RUN apt update \
 && apt install -y socat \
 && apt autoremove -y \
 && apt clean

RUN pip3 install --upgrade pip \
 && pip3 install --upgrade setuptools \
 && pip3 install pyserial \
 && rm -rf ~/.cache/pip

ENV DISPLAY host.docker.internal:0