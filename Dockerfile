FROM python:3.9

WORKDIR /app

COPY requirements/requirements.txt /app

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# using matplotlib inside docker container
RUN apt-get install -y python3-tk

# create dirs for csvs
RUN mkdir -p /app/csvs/xotcen01
RUN mkdir -p /app/csvs/xkubik32
RUN mkdir -p /app/csvs/xkacur04

# create dirs for plots
RUN mkdir -p /app/plots/xotcen01
RUN mkdir -p /app/plots/xkubik32
RUN mkdir -p /app/plots/xkacur04

COPY . /app
