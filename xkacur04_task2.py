from influxdb import InfluxDBClient
from scraper_funcs import connect_to_db, create_and_switch_to_db
import xml.etree.ElementTree as ET
from copy import deepcopy
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import numpy as np
from datetime import datetime
from matplotlib import dates

XML_PATH = './district_codes.xml'

def load_district_data(path):
	with open(path, encoding='Windows-1250') as f:
		xml = (ET.fromstring(f.read())[1])[:-1]
		return {'codes': {item[0][0].text: item[1][0].text for item in xml},
				'names': {item[0][0].text: item[0][1].text for item in xml}}

def task2(client):
	data_infected = list(client.query('select time, okres_lau_kod, kumulativni_pocet_nakazenych from "group_2-kraj-okres-nakazeni-vyleceni-umrti" where time >= \'2020-07-31\' order by time;').get_points())
	data_tests = list(client.query('select time, okres_lau_kod, prirustkovy_pocet_testu_okres from "group_4-kraj-okres-testy" order by time;').get_points())
	data_residents = list(client.query('select hodnota, vuzemi_kod from "group_2-obyvatelstvo" where time=\'2020-12-31\' and pohlavi_kod=\'\' and vek_kod=\'\';').get_points())
	district_data = load_district_data(XML_PATH)

	data_residents_prague = list(filter(lambda x: True if str(x['vuzemi_kod']) == '3018' else False, data_residents))[0]
	data_residents_prague['vuzemi_kod'] = '40924' # correction, prague is not listed as district, only as a region

	data_joined = {}
	for district in district_data['codes'].keys():		
		data_tests_district = list(filter(lambda x: True if x['okres_lau_kod'] == district else False, data_tests))
		data_infected_district = list(filter(lambda x: True if x['okres_lau_kod'] == district else False, data_infected))		
		residents_district = list(filter(lambda x: True if str(x['vuzemi_kod']) == district_data['codes'][district] else False, data_residents))[0]['hodnota']
		
		data_joined_district = []
		for i, date in enumerate(data_tests_district):
			date = deepcopy(date)
			date['nakazeni'] = data_infected_district[i+1]['kumulativni_pocet_nakazenych'] - data_infected_district[i]['kumulativni_pocet_nakazenych']
			date.pop('okres_lau_kod')			
			data_joined_district.append(date)

		data_joined_district_7_days = []
		for i, date in enumerate(data_joined_district[6:]):
			date = deepcopy(date)
			date['nakazeni_7_dni'] = sum([data_joined_district[j]['nakazeni'] for j in range(i-6, i+1)])/7
			date['testy_7_dni'] = sum([data_joined_district[j]['prirustkovy_pocet_testu_okres'] for j in range(i-6, i+1)])/7
			date['pozitivita_7_dni'] = 0 if date['testy_7_dni'] == 0 else date['nakazeni_7_dni'] / date['testy_7_dni']
			date['testy_na_obyvatela_7_dni'] = 0 if date['testy_7_dni'] == 0 else date['nakazeni_7_dni'] / residents_district
			data_joined_district_7_days.append(date)
		data_joined[district] = data_joined_district_7_days

	ratios = []
	for i, (key, data) in enumerate(data_joined.items()):		
		pos = [x['pozitivita_7_dni'] for x in data]
		tests = [x['testy_na_obyvatela_7_dni']*100 for x in data]
		ratio = np.array([0 if x['testy_na_obyvatela_7_dni'] == 0 else x['pozitivita_7_dni'] / x['testy_na_obyvatela_7_dni'] for x in data])
		ratios.append((key, np.mean(ratio)))
	ratios = sorted(ratios, key=lambda x: x[1])

	fig = plt.figure(dpi=200, figsize=(18, 12))
	subfigs = fig.subfigures(nrows=2, ncols=1)
	titles = ['Najlepšie okresy', 'Najhoršie okresy']
	districts_plot = [x[0] for x in ratios[:3] + ratios[-3:]]
	for i, subfig in enumerate(subfigs):
		subfig.suptitle(titles[i], fontsize=18)		
		axes = subfig.subplots(nrows=1, ncols=3, sharey=True)
		for j, ax in enumerate(axes):
			dist_code = districts_plot[i*3 + j]
			data = data_joined[dist_code]
			time = [datetime.strptime(x['time'].split('T')[0], '%Y-%m-%d').date() for x in data]
			pos = [x['pozitivita_7_dni'] for x in data]
			tests = [x['testy_na_obyvatela_7_dni']*100 for x in data]
			df = pd.DataFrame({'Dátum': time, 'Pozitivita': pos, 'Testy na obyv. * 100': tests})
			df = pd.melt(df, 'Dátum', var_name='Hodnoty', value_name='Hodnota')

			ax.set_title(district_data['names'][dist_code])
			ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d'))
			ax.xaxis.set_major_locator(dates.DayLocator(interval=150))
			ax.set_ybound((-0.02, 0.75))
			plot = sns.lineplot(x='Dátum', y='Hodnota', ax=ax, hue='Hodnoty', data=df)

	plt.savefig('xkacur04_task2.png', dpi=200)
