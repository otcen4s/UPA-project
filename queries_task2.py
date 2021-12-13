#!/usr/bin/env python


from influxdb import InfluxDBClient
from datetime import datetime


nuts_Prague = 'CZ010'
nuts_Stredocesky = 'CZ020'
nuts_Jihocesky = 'CZ031'
nuts_Plzensky = 'CZ032'
nuts_Karlovarsky = 'CZ041'
nuts_Ustecky = 'CZ042'
nuts_Liberecky = 'CZ051'
nuts_Kralovehradecky = 'CZ052'
nuts_Pardubicky = 'CZ053'
nuts_Vysocina = 'CZ063'
nuts_Jihomoravsky = 'CZ064'
nuts_Olomoucky = 'CZ071'
nuts_Zlinsky = 'CZ072'
nuts_Moravskoslezsky = 'CZ080'



def task1(client):

    result = client.query('select * from "group_2-kraj-okres-nakazeni-vyleceni-umrti" limit 10 ')


    dates = []

    for point in result.get_points():
        dates.append(datetime.strptime(point['time'][0:10], '%Y-%m-%d'))
        

    print(dates)
    
