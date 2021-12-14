import datetime

import matplotlib.pyplot as plt
import datetime
import numpy as np


def task_1(client):
    graph_1_data = {}
    result = client.query('select "pocet_hosp" from "group_1-hospitalizace"')

    for point in result.get_points():
        graph_1_data.update({
            point['time']: {
                'pocet_hosp': point['pocet_hosp']
            }
        })

    result = client.query('select "prirustkovy_pocet_nakazenych", "prirustkovy_pocet_vylecenych", "prirustkovy_pocet_provedenych_testu" from "group_1-nakazeni-vyleceni-umrti-testy"')

    for point in result.get_points():
        graph_1_data[point['time']] = {
            'nakazeny': point['prirustkovy_pocet_nakazenych'],
            'vylieceny': point['prirustkovy_pocet_vylecenych'],
            'testy': point['prirustkovy_pocet_provedenych_testu']
        }

    #for k, v in graph_1_data.items():
    #    print(f'{k}: {v}')

    x = np.array([datetime.datetime.strptime(record[0:10], '%Y-%m-%d') for record in graph_1_data.keys()])
    y = np.random.randint(100, size=x.shape)

    #x = np.array([datetime.datetime(2013, 9, 28, i, 0) for i in range(24)])
    #y = np.random.randint(100, size=x.shape)

    plt.plot(x, y)
    plt.show()