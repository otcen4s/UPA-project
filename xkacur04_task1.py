from influxdb import InfluxDBClient
from scraper_funcs import connect_to_db, create_and_switch_to_db
import xml.etree.ElementTree as ET
from copy import deepcopy
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from pprint import pprint

XML_PATH = './district_codes.xml'
age_groups = {'0-14': ['400000600005000', '400005610010000', '410010610015000'],
			'15-59': ['410015610020000', '410020610025000', '410025610030000', 
			'410030610035000', '410035610040000', '410040610045000', '410045610050000',
			'410050610055000', '410055610060000']}
region_codes = {'CZ071': '3123',
				'CZ053': '3093',
				'CZ041': '3051',
				'CZ052': '3085',
				'CZ064': '3115',
				'CZ031': '3034',
				'CZ051': '3077',
				'CZ010': '3018',
				'CZ063': '3107',
				'CZ020': '3026',
				'CZ032': '3042',
				'CZ072': '3131',
				'CZ080': '3140',
				'CZ042': '3069'}

def load_district_data(path):
	with open(path, encoding='Windows-1250') as f:
		xml = (ET.fromstring(f.read())[1])[:-1]
		return {'codes': {item[0][0].text: item[1][0].text for item in xml},
				'names': {item[0][0].text: item[0][1].text for item in xml}}

def inverse_dict(old_dict):
	return {y: x for x, y in old_dict.items()}

def replace_prague(data):
	for i, x in enumerate(data):
		if str(x['vuzemi_kod']) == '3018':
			x['vuzemi_kod'] = '40924'
		data[i] = x
	return data

def task1(client):
	data_residents_total = list(client.query('select hodnota, vuzemi_kod from "group_2-obyvatelstvo" where time=\'2020-12-31\' and pohlavi_kod=\'\' and vek_kod=\'\';').get_points())
	data_residents_0_14 = [list(client.query(f'select hodnota, vuzemi_kod from "group_2-obyvatelstvo" where time=\'2020-12-31\' and pohlavi_kod=\'\' and vek_kod=\'{g}\';').get_points()) for g in age_groups['0-14']]
	data_residents_15_59 = [list(client.query(f'select hodnota, vuzemi_kod from "group_2-obyvatelstvo" where time=\'2020-12-31\' and pohlavi_kod=\'\' and vek_kod=\'{g}\';').get_points()) for g in age_groups['15-59']]	
	data_infected_start = list(client.query('select time, okres_lau_kod, kumulativni_pocet_nakazenych from "group_2-kraj-okres-nakazeni-vyleceni-umrti" where time = \'2020-12-27\';').get_points())
	data_infected_end = list(client.query('select time, okres_lau_kod, kumulativni_pocet_nakazenych from "group_2-kraj-okres-nakazeni-vyleceni-umrti" where time = \'2021-12-13\';').get_points())
	
	for i, x in enumerate(data_residents_0_14):
		data_residents_0_14[i] = replace_prague(x)
	for x in data_residents_15_59:
		data_residents_15_59[i] = replace_prague(x)

	data_vaccinated = client.query('select sum(celkem_davek) from "group_5-ockovani" group by kraj_nuts_kod, kraj_nuts_kod;')
	data_vaccinated = {x[0][1]['kraj_nuts_kod']: list(x[1])[0]['sum'] for x in data_vaccinated.items()}
	
	data_residents_regions = {inverse_dict(region_codes)[x['vuzemi_kod']]: x['hodnota'] for x in list(filter(lambda x: x['vuzemi_kod'] in region_codes.values(), data_residents_total))}
	ratio_vaccinated_districts = {}

	district_data = load_district_data(XML_PATH)
	for region, vaccinated in data_vaccinated.items():
		residents = data_residents_regions[region]
		ratio = vaccinated / residents
		districts_region = list(filter(lambda x: region in x, district_data['codes'].keys()))
		ratio_vaccinated_districts = {**ratio_vaccinated_districts, **{x: ratio for x in districts_region}}
	
	data_residents_total = replace_prague(data_residents_total)
	data_districts = []
	for key, value in district_data['codes'].items():
		residents_0_14 = sum([x['hodnota'] for x in [x for y in list(map(lambda x: list(filter(lambda y: y['vuzemi_kod'] == value, x)), data_residents_0_14)) for x in y]])
		residents_15_59 = sum([x['hodnota'] for x in [x for y in list(map(lambda x: list(filter(lambda y: y['vuzemi_kod'] == value, x)), data_residents_15_59)) for x in y]])
		residents_total = list(filter(lambda x: x['vuzemi_kod'] == value, data_residents_total))[0]['hodnota']
		ratio_0_14 = residents_0_14 / residents_total
		ratio_15_59 = residents_15_59 / residents_total

		infected_start = list(filter(lambda x: x['okres_lau_kod'] == key, data_infected_start))[0]['kumulativni_pocet_nakazenych']
		infected_end = list(filter(lambda x: x['okres_lau_kod'] == key, data_infected_end))[0]['kumulativni_pocet_nakazenych']
		ratio_infected = (infected_end - infected_start) / residents_total
		ratio_vaccinated = ratio_vaccinated_districts[key]
		data_districts.append([ratio_0_14, ratio_15_59, ratio_infected, ratio_vaccinated])

	N_CLUSTERS = 4
	kmeans = KMeans(n_clusters=N_CLUSTERS).fit(data_districts)
	clusters = {str(i): [] for i in range(N_CLUSTERS)}
	for i, district in enumerate(district_data['names'].values()):
		clusters[str(kmeans.labels_[i])].append(district)
	with open('xkacur04_task1.txt', 'w') as f:
		pprint(clusters, f)
