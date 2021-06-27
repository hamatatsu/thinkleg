# syntax=docker/dockerfile:1

FROM python:3.7.5

RUN apt update \
 && apt install -y socat \
 && apt autoremove \
 && apt clean

WORKDIR /workspace/raspi-src
ADD requirements.txt /workspace/raspi-src

RUN pip3 install -U pip \
 && pip3 install -U setuptools \
 && pip3 install --no-cache-dir -r requirements.txt

ENV DISPLAY host.docker.internal:0