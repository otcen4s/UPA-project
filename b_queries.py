#!/usr/bin/env python

from datetime import datetime
import csv
import matplotlib.pyplot as plt
from numpy.lib.function_base import diff
import pandas as pd
import numpy as np
import plotly.express as px
from b_queries_plot import plot_graph_task1, plot_graph_task2_deaths_line, plot_graph_task2_deaths_bar, plot_graph_task2_hospit_bar, plot_graph_task2_hospit_line


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


def export_to_csv(data, name, header):
    
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
        difference_dict[kraj].insert(0,0)
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
                        record["prirastok"] = difference_dict[item[0][1]["kraj_nuts_kod"]][i]
                            
                        i += 1

                        record_copy = record.copy()
                        quartal_list.append(record_copy)

    return quartal_list


def csv_data1(quartal):
    data = []
    for record in quartal:
        line = [record["datum"], record["kraj"], record["pocet_nakazenych_per_capita"], record["celkovy_pocet_nakazenych"], record["celkovy_pocet_obyvatelov"], record["prirastok"]]
        data.append(line)
    
    return data


def task1(client):
    result_quartal1, result_quartal2, result_quartal3, result_quartal4 = get_quartals(client)

    quartal1 = record_merge(result_quartal1)
    quartal2 = record_merge(result_quartal2)
    quartal3 = record_merge(result_quartal3)
    quartal4 = record_merge(result_quartal4)

    data1 = csv_data1(quartal1)
    data2 = csv_data1(quartal2)
    data3 = csv_data1(quartal3)
    data4 = csv_data1(quartal4)

    header = ['datum', 'kraj', 'pocet_nakazenych_per_capita', 'celkovy_pocet_nakazenych', 'celkovy_pocet_obyvatelov', 'prirastok']

    export_to_csv(data1, "csvs/xotcen01/first_quartal.csv", header)
    export_to_csv(data2, "csvs/xotcen01/second_quartal.csv", header)
    export_to_csv(data3, "csvs/xotcen01/third_quartal.csv", header)
    export_to_csv(data4, "csvs/xotcen01/fourth_quartal.csv", header)

    plot_graph_task1("csvs/xotcen01/first_quartal.csv", "plots/xotcen01/prvy_kvartal", "Obdobie pre štvrtý kvartál ")
    plot_graph_task1("csvs/xotcen01/second_quartal.csv", "plots/xotcen01/druhy_kvartal", "Obdobie pre tretí kvartál ")
    plot_graph_task1("csvs/xotcen01/third_quartal.csv", "plots/xotcen01/treti_kvartal", "Obdobie pre druhý kvartál ")
    plot_graph_task1("csvs/xotcen01/fourth_quartal.csv", "plots/xotcen01/stvrty_kvartal", "Obdobie pre prvý kvartál ")





################################################################
################################################################
################################################################


def csv_data2(quartal):
    data = []
    for record in quartal:
        line = [record["datum"], record["umrti_celkom"], record["neockovani"], record["jedna_davka"], record["zaockovani"]]
        data.append(line)
    
    return data

def csv_data3(quartal):
    data = []
    for record in quartal:
        line = [record["datum"], record["hospitalizovani_celkom"], record["neockovani"], record["jedna_davka"], record["zaockovani"]]
        data.append(line)
    
    return data

def task2_queries(client):
    hospitalizations = client.query('SELECT "hospitalizovani_celkem","hospitalizovani_bez_ockovani","hospitalizovani_nedokoncene_ockovani","hospitalizovani_dokoncene_ockovani" FROM "group_3-ockovani-hospitalizace" WHERE time > now() - 365d') # last year
    deaths = client.query('SELECT "zemreli_celkem","zemreli_bez_ockovani","zemreli_nedokoncene_ockovani","zemreli_dokoncene_ockovani" FROM "group_3-ockovani-umrti" WHERE time > now() - 365d') # last year

    return hospitalizations, deaths


def merge_deaths(deaths):
    record = {}
    deaths_list = []
    
    for point in deaths.get_points():
        record["datum"] = str(point['time'][0:10])
        record["umrti_celkom"] = point['zemreli_celkem']
        record["neockovani"] = point['zemreli_bez_ockovani']
        record["jedna_davka"] = point['zemreli_nedokoncene_ockovani']
        record["zaockovani"] = point['zemreli_dokoncene_ockovani']

        record_copy = record.copy()
        deaths_list.append(record_copy)
    
    return deaths_list


def merge_hospitalizations(hospitalizations):
    record = {}
    hospitalizations_list = []
    
    for point in hospitalizations.get_points():
        record["datum"] = str(point['time'][0:10])
        record["hospitalizovani_celkom"] = point['hospitalizovani_celkem']
        record["neockovani"] = point['hospitalizovani_bez_ockovani']
        record["jedna_davka"] = point['hospitalizovani_nedokoncene_ockovani']
        record["zaockovani"] = point['hospitalizovani_dokoncene_ockovani']

        record_copy = record.copy()
        hospitalizations_list.append(record_copy)
    
    return hospitalizations_list


def task2(client):
    
    hospitalizations, deaths = task2_queries(client)

    deaths = merge_deaths(deaths)
    data_deaths = csv_data2(deaths)
    header = ['datum', 'umrti_celkom', 'neockovani', 'jedna_davka', 'zaockovani']
    export_to_csv(data_deaths, "csvs/xotcen01/deaths.csv", header)

    hospitalizations = merge_hospitalizations(hospitalizations)
    data_hospitalizations = csv_data3(hospitalizations)
    header = ['datum', 'hospitalizovani_celkom', 'neockovani', 'jedna_davka', 'zaockovani']
    export_to_csv(data_hospitalizations, "csvs/xotcen01/hospitalizations.csv", header)


    plot_graph_task2_deaths_bar("csvs/xotcen01/deaths.csv", "plots/xotcen01/umrtia_november_bar", "Úmrtia na COVID od začiatku Novembra po aktuálny deň", range='2021-11-01', range_set=True)
    plot_graph_task2_hospit_bar("csvs/xotcen01/hospitalizations.csv", "plots/xotcen01/hospitalizacie_november_bar", "Hospitalizácie na COVID od začiatku Novembra po aktuálny deň", range='2021-11-01', range_set=True)

    plot_graph_task2_deaths_line("csvs/xotcen01/deaths.csv", "plots/xotcen01/umrtia_november_line", "Úmrtia na COVID od začiatku Novembra po aktuálny deň", range='2021-11-01', range_set=True)
    plot_graph_task2_hospit_line("csvs/xotcen01/hospitalizations.csv", "plots/xotcen01/hospitalizacie_november_line", "Hospitalizácie na COVID od začiatku Novembra po aktuálny deň", range='2021-11-01', range_set=True)


    plot_graph_task2_deaths_line("csvs/xotcen01/deaths.csv", "plots/xotcen01/umrtia_line", "Úmrtia na COVID za posledný rok")
    plot_graph_task2_hospit_line("csvs/xotcen01/hospitalizations.csv", "plots/xotcen01/hospitalizacie_line", "Hospitalizácie na COVID za posledný rok")

    plot_graph_task2_deaths_bar("csvs/xotcen01/deaths.csv", "plots/xotcen01/umrtia_bar", "Úmrtia na COVID za posledný rok")
    plot_graph_task2_hospit_bar("csvs/xotcen01/hospitalizations.csv", "plots/xotcen01/hospitalizacie_bar", "Hospitalizácie na COVID za posledný rok")



