FROM python:3.7-alpine3.7

RUN echo "http://dl-4.alpinelinux.org/alpine/v3.7/main" >> /etc/apk/repositories && \
    echo "http://dl-4.alpinelinux.org/alpine/v3.7/community" >> /etc/apk/repositories

RUN apk update && apk add build-base git chromium chromium-chromedriver

RUN mkdir /src
WORKDIR /src
COPY ./src /src

RUN pip3 install --no-cache-dir -r requirements.txt
