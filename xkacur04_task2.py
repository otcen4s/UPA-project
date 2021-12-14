from influxdb import InfluxDBClient
from scraper_funcs import connect_to_db, create_and_switch_to_db
import xml.etree.ElementTree as ET
from copy import deepcopy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
	fig, axes = plt.subplots(2, 3, figsize=(12, 8), dpi=200, sharey=True)
	for i, x in enumerate(ratios[:3] + ratios[-3:]):
		data = data_joined[x[0]]
		time = [x['time'] for x in data]
		pos = [x['pozitivita_7_dni'] for x in data]
		tests = [x['testy_na_obyvatela_7_dni']*100 for x in data]
		df = pd.DataFrame({'time': time, 'positivity': pos, 'tests': tests})
		df = pd.melt(df, 'time', var_name='Measure', value_name='Value')
		plot = sns.lineplot('time', 'Value', ax=axes[i//3, i%3], hue='Measure', data=df)
		plot.set(xticklabels=[], xticks=[])
		axes[i//3, i%3].set_title(district_data['names'][x[0]])

	plt.savefig('xkacur04_task2.png', dpi=200)
