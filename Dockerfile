FROM python:3.9

WORKDIR /app

COPY requirements/requirements.txt /app

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# using matplotlib inside docker container
RUN apt-get install -y python3-tk

RUN echo $(id -u $USER):$(id -g $USER)

COPY . /app
