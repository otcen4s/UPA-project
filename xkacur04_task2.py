from influxdb import InfluxDBClient
from scraper_funcs import connect_to_db, create_and_switch_to_db
import xml.etree.ElementTree as ET
from copy import deepcopy

XML_PATH = './district_codes.xml'

def load_district_codes(path):
	with open(path, encoding='Windows-1250') as f:
		return {item[0][0].text: item[1][0].text for item in (ET.fromstring(f.read())[1])[:-1]}

def task2(client):
	data_infected = client.query('select time, okres_lau_kod, kumulativni_pocet_nakazenych from "group_2-kraj-okres-nakazeni-vyleceni-umrti" where time >= \'2020-07-31\' order by time;').get_points()
	data_tests = client.query('select time, okres_lau_kod, prirustkovy_pocet_testu_okres from "group_4-kraj-okres-testy" order by time;').get_points()
	#data_residents = client.query('select * from "group_2-obyvatelstvo" where time = \'2020-12-31\';').get_points()
	district_codes = load_district_codes(XML_PATH)

	data_infected = list(data_infected)
	data_tests = list(data_tests)
	print(len(list(data_residents)))

	data_joined = {}
	for district in district_codes.keys():		
		data_tests_district = list(filter(lambda x: True if x['okres_lau_kod'] == district else False, data_tests))
		data_infected_district = list(filter(lambda x: True if x['okres_lau_kod'] == district else False, data_infected))
		
		data_joined_district = []
		for i, date in enumerate(data_tests_district):
			date = deepcopy(date)
			date['nakazeni'] = data_infected_district[i+1]['kumulativni_pocet_nakazenych'] - data_infected_district[i]['kumulativni_pocet_nakazenych']
			date.pop('okres_lau_kod')
			date['pozitivita'] = 0 if date['prirustkovy_pocet_testu_okres'] == 0 else date['nakazeni'] / date['prirustkovy_pocet_testu_okres']
			data_joined_district.append(date)
		data_joined[district] = data_joined_district
