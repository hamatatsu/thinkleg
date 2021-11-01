# syntax=docker/dockerfile:1

FROM python:3.7.5-alpine

RUN apk --update add socat

RUN pip3 install -U pip \
 && pip3 install -U setuptools \
 && pip3 install --no-cache-dir pyserial

WORKDIR /workspace/arduino-emu