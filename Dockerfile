
FROM python:3.7-alpine3.8
MAINTAINER Artur Bartecki

# Create project and set project scope
RUN mkdir /code
WORKDIR /code

# Install chromedriver
RUN apk update
RUN apk add chromium chromium-chromedriver

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt
