#!/usr/bin/env python

from scraper_funcs import (connect_to_db, create_and_switch_to_db, download_csv_data,
                           prepare_xml_data_for_db, prepare_csv_data_for_db, save_data_to_db)

data_groups = {
    'group_1': {
        'dataset_1': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv',
        'dataset_2': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv',
    },
    'group_2': {
        'dataset_1': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv',
        # non time series data uses fake time for saving it to influx db
        'dataset_2': 'https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv/760fab9c-d079-4d3a-afed-59cbb639e37d?version=1.1',
    },
    'group_3': {
        'dataset_1': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-umrti.csv',
        'dataset_2': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-pozitivni.csv',
    },
    'group_4': {
        'dataset_1': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv',
        'dataset_2': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-testy.csv',
        'dataset_3': 'https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv',
        # 'dataset_4': 'https://apl.czso.cz/iSMS/cisexp.jsp?kodcis=109&typdat=1&cisvaz=101_1768&cisjaz=203&format=0',
    },
    'group_5': {
        'dataset_1': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv',
        'dataset_2': 'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv',
    }
}


def main():
    upa_proj_db = "covid-19"
    client = connect_to_db()

    create_and_switch_to_db(client, upa_proj_db)

    enum = 0
    for group_name, datasets in data_groups.items():
        enum += 1
        for dataset, url in datasets.items():
            print(dataset, url)
            print(f"{group_name}-{dataset}")

            csv_reader = download_csv_data(url)

            measurement = f"{group_name}-{dataset}"
            if measurement == 'group_4-dataset_4':
                continue
                data_for_saving_to_db = prepare_xml_data_for_db(measurement, csv_reader)  # TODO
            else:
                data_for_saving_to_db = prepare_csv_data_for_db(measurement, csv_reader)

            save_data_to_db(client, data_for_saving_to_db)


if __name__ == '__main__':
    main()
