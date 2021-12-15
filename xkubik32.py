import csv
import datetime

import matplotlib.pyplot as plt
import numpy as np


def save_csv(filename, fieldnames, data, key):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for k, row in data.items():
            row.update({key: k})
            writer.writerow(row)


def task_a_1_save_csv(client, filename):
    graph_data = {}

    result = client.query('select sum("prirustkovy_pocet_nakazenych"), sum("prirustkovy_pocet_vylecenych"), sum("prirustkovy_pocet_provedenych_testu") from "group_1-nakazeni-vyleceni-umrti-testy"  where time >=\'2020-03-01T00:00:00Z\'  and time <= \'2021-11-30T00:00:00Z\'  group by time(31d)')

    for point in result.get_points():
        point["time"] = datetime.datetime.strptime(point["time"][0:10], "%Y-%m-%d").date()
        graph_data[point["time"]] = {
            "nakazeny": point["sum"],
            "vylieceny": point["sum_1"],
            "testy": point["sum_2"],
        }

    result = client.query(
        'select sum("pocet_hosp") from "group_1-hospitalizace" where time >=\'2020-03-01T00:00:00Z\'  and time <=\'2021-11-30T00:00:00Z\'  group by time(31d)')

    for point in result.get_points():
        point["time"] = datetime.datetime.strptime(point["time"][0:10], "%Y-%m-%d").date()
        graph_data[point["time"]]["pocet_hosp"] = float(point["sum"])

    fieldnames = ["date", "pocet_hosp", "nakazeny", "vylieceny", "testy"]
    save_csv(filename, fieldnames, graph_data, "date")


def task_a_1_plot_csv(filename):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        dates = []
        hospitalizovany = []
        nakazeny = []
        vylieceny = []
        testy = []

        for row in reader:
            dates.append(datetime.datetime.strptime(row["date"], "%Y-%m-%d"))
            hospitalizovany.append(float(row["pocet_hosp"]))
            nakazeny.append(float(row["nakazeny"]))
            vylieceny.append(float(row["vylieceny"]))
            testy.append(float(row["testy"]))

    plt.figure(figsize=(8, 8))
    plt.title("Vyvoj covidovej situacie po mesiacoch")
    plt.xticks(rotation=45)
    plt.plot(dates, nakazeny, label="nakazeny")
    plt.plot(dates, vylieceny, label="vylieceny")
    plt.legend(loc="best")

    plt.savefig("task_a_1_1.jpg")
    plt.show()

    plt.figure(figsize=(8, 8))
    plt.title("Vyvoj covidovej situacie po mesiacoch")
    plt.xticks(rotation=45)
    plt.plot(dates, testy, label="testy")
    plt.legend(loc="best")

    plt.savefig("task_a_1_2.jpg")
    plt.show()

    plt.figure(figsize=(8, 8))
    plt.title("Vyvoj covidovej situacie po mesiacoch")
    plt.xticks(rotation=45)
    plt.plot(dates, hospitalizovany, label="hospitalizovany")
    plt.legend(loc="best")

    plt.savefig("task_a_1_3.jpg")
    plt.show()


NUTS = {
    "CZ010": "Praha",
    "CZ020": "Stredocesky",
    "CZ031": "Jihocesky",
    "CZ032": "Plzensky",
    "CZ041": "Karlovarsky",
    "CZ042": "Ustecky",
    "CZ051": "Liberecky",
    "CZ052": "Kralovehradecky",
    "CZ053": "Pardubicky",
    "CZ063": "Vysocina",
    "CZ064": "Jihomoravsky",
    "CZ071": "Olomoucky",
    "CZ072": "Zlinsky",
    "CZ080": "Moravskoslezsky"
}


def select_and_udpate_data(client, query, data, key):
    result = client.query(query)
    for k, v in result.items():
        kraj = NUTS.get(k[1]["kraj_nuts_kod"])
        if kraj:
            data[kraj].update({key: list(v)[0]["count"]})


def task_a_2_save_csv(client, filename):
    graph_data = {v: {} for v in NUTS.values()}
    query_1 = 'select count(id) from "group_5-osoby" where  "vek"<=15 group by "kraj_nuts_kod"'
    select_and_udpate_data(client, query_1, graph_data, "<15")

    query_2 = 'select count(id) from "group_5-osoby" where  "vek">15 and "vek"<=30 group by "kraj_nuts_kod"'
    select_and_udpate_data(client, query_2, graph_data, "<30")

    query_3 = 'select count(id) from "group_5-osoby" where  "vek">30 and "vek"<=45 group by "kraj_nuts_kod"'
    select_and_udpate_data(client, query_3, graph_data, "<45")

    query_4 = 'select count(id) from "group_5-osoby" where  "vek">45 and "vek"<=60 group by "kraj_nuts_kod"'
    select_and_udpate_data(client, query_4, graph_data, "<60")

    query_5 = 'select count(id) from "group_5-osoby" where  "vek">60 group by "kraj_nuts_kod"'
    select_and_udpate_data(client, query_5, graph_data, ">60")

    fieldnames = ["kraj", "<15", "<30", "<45", "<60", ">60"]
    save_csv(filename, fieldnames, graph_data, "kraj")


def task_a_2_plot_csv(filename):
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        kraj = []
        group_1 = []  # <15
        group_2 = []  # <30
        group_3 = []  # <45
        group_4 = []  # <60
        group_5 = []  # >60

        for row in reader:
            kraj.append(row["kraj"])
            group_1.append(float(row["<15"]))
            group_2.append(float(row["<30"]))
            group_3.append(float(row["<45"]))
            group_4.append(float(row["<60"]))
            group_5.append(float(row[">60"]))

    group_1 = np.array(group_1)
    group_2 = np.array(group_2)
    group_3 = np.array(group_3)
    group_4 = np.array(group_4)
    group_5 = np.array(group_5)

    plt.figure(figsize=(8, 8))
    plt.bar(kraj, group_1, label="<15")
    plt.bar(kraj, group_2, bottom=group_1, label="<30")
    plt.bar(kraj, group_3, bottom=group_1 + group_2, label="<45")
    plt.bar(kraj, group_4, bottom=group_1 + group_2 + group_3, label="<60")
    plt.bar(kraj, group_5, bottom=group_1 + group_2 + group_3 + group_4, label=">60")

    plt.xlabel("Kraj")
    plt.xticks(rotation=45)
    plt.ylabel("Pocet nakazenych")
    plt.title("Rozlozenie veku nakazenych v jednotlivych krajoch")
    plt.legend()
    plt.savefig("task_a_2.jpg")
    plt.show()


def task_a_1(client):
    filename = "task_a_1.csv"
    task_a_1_save_csv(client, filename)
    task_a_1_plot_csv(filename)


def task_a_2(client):
    filename = "task_a_2.csv"
    task_a_2_save_csv(client, filename)
    task_a_2_plot_csv(filename)
