import os
import csv
from datetime import datetime, timedelta

import rfc3339
import requests
from influxdb import InfluxDBClient


def connect_to_db():
    host = os.getenv('INFLUX_HOST')
    port = os.getenv('INFLUX_PORT')
    login = os.getenv('INFLUX_LOGIN')
    password = os.getenv('INFLUX_PASSWORD')

    default_db = "_internal"  # default system db

    return InfluxDBClient(host, port, login, password, default_db)


def create_and_switch_to_db(client, db_name):
    print(f"Create database: {db_name}")
    client.create_database(db_name)

    print(f"Switch to database: {db_name}")
    client.switch_database(db_name)


def convert_date_to_rfc3339_format(date):
    if isinstance(date, str):
        date = datetime.fromisoformat(date)
    return rfc3339.rfc3339(date)


def download_csv_data(url):
    return requests.get(url).content.decode('utf-8-sig')


def prepare_csv_data_for_db(measurement, data):
    # fake date is for saving non time series data to time series DB
    fake_date = '1970-01-01'
    fake_date = datetime.fromisoformat(fake_date)

    data_for_db = []
    csv_reader = csv.DictReader(data.split('\n'))
    for record in csv_reader:
        try:
            date = record.pop("datum")
        except KeyError:
            date = fake_date
            fake_date += timedelta(days=1)

        data_for_db.append({
            "measurement": measurement,
            "time": convert_date_to_rfc3339_format(date),
            "fields": record
        })

    return data_for_db


# TODO: parse xml data and prepare for saving to db
def prepare_xml_data_for_db(measurement, data):
    pass


def save_data_to_db(client, data):
    client.write_points(data)
