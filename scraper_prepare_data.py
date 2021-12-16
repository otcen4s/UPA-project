import csv

from scraper_funcs import convert_date_to_rfc3339_format


def remove_unwanted_columns(record, unwanted_columns):
    """Remove data with unwanted columns from record for saving to db."""
    for column in unwanted_columns:
        record.pop(column)

    return record


def prepare_data_for_db(measurement, csv_data, unwanted_columnts=[], tags_columns=None, date_column="datum", now=False):
    """Prepare downloaded csv file for saving to db. """
    global_date = 1639526785000000000

    data_for_db = []
    csv_reader = csv.DictReader(csv_data.split("\n"))
    for record in csv_reader:
        record = remove_unwanted_columns(record, unwanted_columnts)

        date = record.pop(date_column)

        if tags_columns:
            tags = {}
            for column in tags_columns:
                rec = record.pop(column[0])
                try:
                    tags.update({column[0]: column[1](rec)})
                except ValueError:  # jump over records with empty data
                    pass

        # all items are saved as integer
        for k, v in record.items():
            try:
                record[k] = int(v)
            except ValueError:
                record[k] = 0

        if now:
            global_date += 1
            date = global_date

        data_for_db.append({
            "measurement": measurement,
            "time": global_date if now else convert_date_to_rfc3339_format(date),
            "fields": record
        })

        if tags_columns:
            data_for_db[-1].update({"tags": tags})

    return data_for_db
