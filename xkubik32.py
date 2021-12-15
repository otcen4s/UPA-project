import datetime
import csv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

import datetime
import numpy as np


def task_1_save_csv(client, filename):
    graph_1_data = {}

    result = client.query('select sum("prirustkovy_pocet_nakazenych"), sum("prirustkovy_pocet_vylecenych"), sum("prirustkovy_pocet_provedenych_testu") from "group_1-nakazeni-vyleceni-umrti-testy"  where time >=\'2020-03-01T00:00:00Z\'  and time <= \'2021-11-30T00:00:00Z\'  group by time(31d)')

    for point in result.get_points():
        point['time'] = datetime.datetime.strptime(point['time'][0:10], '%Y-%m-%d').date()
        print(point['time'])
        print(point)
        graph_1_data[point['time']] = {
            'nakazeny': point['sum'],
            'vylieceny': point['sum_1'],
            'testy': point['sum_2'],
        }

    result = client.query(
        'select sum("pocet_hosp") from "group_1-hospitalizace" where time >=\'2020-03-01T00:00:00Z\'  and time <=\'2021-11-30T00:00:00Z\'  group by time(31d)')

    for point in result.get_points():
        point['time'] = datetime.datetime.strptime(point['time'][0:10], '%Y-%m-%d').date()
        graph_1_data[point['time']]['pocet_hosp'] = float(point['sum'])

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'pocet_hosp', 'nakazeny', 'vylieceny', 'testy']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for date, row in graph_1_data.items():
            print(row)
            row.update({'date': date})
            writer.writerow(row)


def task_1_plot_csv(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dates = []
        hospitalizovany = []
        nakazeny = []
        vylieceny = []
        testy = []

        for row in reader:
            dates.append(datetime.datetime.strptime(row['date'], '%Y-%m-%d'))
            hospitalizovany.append(float(row['pocet_hosp']))
            nakazeny.append(float(row['nakazeny']))
            vylieceny.append(float(row['vylieceny']))
            testy.append(float(row['testy']))

    for x in nakazeny:
        print(x)

    print(dates)
    plt.title('Vyvoj covidovej situacie po mesiacoch')
    plt.figure(figsize=(8, 8))
    plt.xticks(rotation=45)
    plt.plot(dates, nakazeny, label='nakazeny')
    plt.plot(dates, vylieceny, label='vylieceny')
    plt.legend(loc='best')

    plt.savefig('task_1_1.jpg')
    plt.show()

    plt.title('Vyvoj covidovej situacie po mesiacoch')
    plt.figure(figsize=(8, 8))
    plt.xticks(rotation=45)
    plt.plot(dates, testy, label='testy')
    plt.legend(loc='best')

    plt.savefig('task_1_2.jpg')
    plt.show()

    plt.title('Vyvoj covidovej situacie po mesiacoch')
    plt.figure(figsize=(8, 8))
    plt.xticks(rotation=45)
    plt.plot(dates, hospitalizovany, label='hospitalizovany')
    plt.legend(loc='best')

    plt.savefig('task_1_3.jpg')
    plt.show()


def task_1(client):
    filename = 'task_A_1.csv'
    task_1_save_csv(client, filename)
    task_1_plot_csv(filename)
