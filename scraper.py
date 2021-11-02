#!/usr/bin/env python

import os

from influxdb import InfluxDBClient


if __name__ == '__main__':
    host = os.getenv('INFLUX_HOST')
    port = os.getenv('INFLUX_PORT')
    login = os.getenv('INFLUX_LOGIN')
    password = os.getenv('INFLUX_PASSWORD')
    dbname = 'example'

    query = 'select Float_value from cpu_load_short;'
    query_where = 'select Int_value from cpu_load_short where host=$host;'
    bind_params = {'host': 'server01'}

    client = InfluxDBClient(host, port, login, password, dbname)

    print("Create database: " + dbname)
    client.create_database(dbname)

    json_body = [
        {
            "measurement": "cpu_load_short",
            "tags": {
                "host": "server01",
                "region": "us-west"
            },
            "time": "2021-11-01T23:00:00Z",
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]

    client.write_points(json_body)

    print(f"Querying data: {query}")
    result = client.query(query)
    print(f"Result: {result}")

    print(f"Querying data: {query_where}")
    result = client.query(query_where, bind_params=bind_params)
    print(f"Result: {result}")
