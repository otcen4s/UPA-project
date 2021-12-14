#!/usr/bin/env python

from datetime import datetime
import csv
import matplotlib.pyplot as plt
from numpy.lib.function_base import diff
import pandas as pd
import numpy as np


NUTS = {'CZ010': [1335084, "Praha"],
        'CZ020': [1397997, "Stredocesky"],
        'CZ031': [643551, "Jihocesky"],
        'CZ032': [591041, "Plzensky"],
        'CZ041': [293311, "Karlovarsky"],
        'CZ042': [817004, "Ustecky"],
        'CZ051': [442476, "Liberecky"],
        'CZ052': [550803, "Kralovehradecky"],
        'CZ053': [522856, "Pardubicky"],
        'CZ063': [508852, "Vysocina"],
        'CZ064': [1195327, "Jihomoravsky"],
        'CZ071': [630522, "Olomoucky"],
        'CZ072': [580119, "Zlinsky"],
        'CZ080': [1192834, "Moravskoslezsky"]
}


def export_to_csv(data, name):
    #TODO nevytvaraju sa CSV aj ked je vsetko ok

    header = ['datum', 'kraj', 'pocet_nakazenych_per_capita', 'celkovy_pocet_nakazenych', 'celkovy_pocet_obyvatelov']

    with open(name, 'w', encoding='UTF8', newline='') as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(data)


def get_quartals(client):
    result_quartal1 = client.query('SELECT SUM("kumulativni_pocet_nakazenych") FROM "group_2-kraj-okres-nakazeni-vyleceni-umrti" WHERE time > now() - 91d GROUP BY time(1d), "kraj_nuts_kod"') # last 3 months
    result_quartal2 = client.query('SELECT SUM("kumulativni_pocet_nakazenych") FROM "group_2-kraj-okres-nakazeni-vyleceni-umrti" WHERE time > now() - 182d AND time <= now() - 91d GROUP BY time(1d), "kraj_nuts_kod"') # between last 3-6 months
    result_quartal3 = client.query('SELECT SUM("kumulativni_pocet_nakazenych") FROM "group_2-kraj-okres-nakazeni-vyleceni-umrti" WHERE time > now() - 273d AND time <= now() - 182d GROUP BY time(1d), "kraj_nuts_kod"') # between last 6-9 months
    result_quartal4 = client.query('SELECT SUM("kumulativni_pocet_nakazenych") FROM "group_2-kraj-okres-nakazeni-vyleceni-umrti" WHERE time > now() - 365d AND time <= now() - 273d GROUP BY time(1d), "kraj_nuts_kod"') # between last 9-12 months

    return result_quartal1, result_quartal2, result_quartal3, result_quartal4

# recount per one person
def per_capita(region, infected):
    return (infected / NUTS[region][0])

def record_merge(quartal):
    record = {}
    quartal_list = []
    difference = []
    kraj = ""
    difference_dict = {}

    for item in list(quartal.items()):
        for point in item[1]:
            if item[0][1] is not None:
                if len(item[0][1]["kraj_nuts_kod"]):
                    if point["sum"] is not None:
                        difference.append(int(point["sum"]))
                        kraj = item[0][1]["kraj_nuts_kod"]

        difference_dict[kraj] = [j-i for i, j in zip(difference[:-1], difference[1:])]
        difference = []

    
    difference_dict = {k:v for k,v in difference_dict.items() if v}


    for item in list(quartal.items()):
        i = 0
        for point in item[1]:
            if item[0][1] is not None:
                if len(item[0][1]["kraj_nuts_kod"]):
                    if point["sum"] is not None:
                        record["datum"] = str(point['time'][0:10])
                        record["kraj"] = NUTS[str(item[0][1]["kraj_nuts_kod"])][1]
                        record["pocet_nakazenych_per_capita"] = per_capita(str(item[0][1]["kraj_nuts_kod"]), int(point["sum"]))
                        record["celkovy_pocet_nakazenych"] = int(point["sum"])
                        record["celkovy_pocet_obyvatelov"] = NUTS[str(item[0][1]["kraj_nuts_kod"])][0]
                        print(len(difference_dict[item[0][1]["kraj_nuts_kod"]]))
                        #record["prirastok"] = difference_dict[item[0][1]["kraj_nuts_kod"]][i]

                        #print(difference_dict[item[0][1]["kraj_nuts_kod"]][i])
                        i += 1

                        record_copy = record.copy()
                        quartal_list.append(record_copy)

    return quartal_list


def task1(client):

    result_quartal1, result_quartal2, result_quartal3, result_quartal4 = get_quartals(client)

    quartal1 = record_merge(result_quartal1)
    quartal2 = record_merge(result_quartal2)
    quartal3 = record_merge(result_quartal3)
    quartal4 = record_merge(result_quartal4)

    data1 = csv_data(quartal1)
    data2 = csv_data(quartal2)
    data3 = csv_data(quartal3)
    data4 = csv_data(quartal4)

    export_to_csv(data1, "first_quartal.csv")
    export_to_csv(data2, "second_quartal.csv")
    export_to_csv(data3, "third_quartal.csv")
    export_to_csv(data4, "fourth_quartal.csv")

def csv_data(quartal):
    data = []
    for record in quartal:
        line = [record["datum"], record["kraj"], record["pocet_nakazenych_per_capita"], record["celkovy_pocet_nakazenych"], record["celkovy_pocet_obyvatelov"], record["prirastok"]]
        data.append(line)
    
    return data



def plot_graph():
    data = pd.read_csv('first_quartal.csv')


    