from scraper_funcs import download_csv_data
from scraper_prepare_data import prepare_data_for_db


def save_data_to_db(dbclient, data):
    dbclient.write_points(data)


def show_schema(data_for_db):
    """Show schema of data for saving to db."""
    if len(data_for_db) > 0:
        print("-------------------------" * 3)
        print(f"{data_for_db[0]['measurement']} schema:")
        print("-------------------------" * 3)

        print(f"measurement: {data_for_db[0]['measurement']}")

        print(f"time: {type(data_for_db[0]['time'])}")

        fields = ""
        for k, v in data_for_db[0]["fields"].items():
            fields += f"{k}: {type(v)}, "
        print(f"fields: {fields}")

        tags = ""
        if data_for_db[0].get("tags"):
            for k, v in data_for_db[0]["tags"].items():
                tags += f"{k}: {type(v)}, "
        print(f"tags: {tags}")


def save_group_1_to_db(dbclient, urls):
    """Save group_1 to influx DB.

    column name(data type) SAVED_AS
    SAVED_AS -> T-tag, F-field, TM-time

    Save `hospitalizace.csv`:
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    datum(date) TM| jip(int) F| kum_umrti(int) F| kyslik(int) F| pocet_hosp(int) F| stav_bez_priznaku(int) F| stav_lehky(int) F| stav_stredni(int) F| stav_tezky(int) F| umrti(int) F
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Save `nakazeni-vyleceni-umrti-testy.csv`:
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    datum(date) TM| kumulativni_pocet_nakazenych(int) F| kumulativni_pocet_vylecenych(int) F| kumulativni_pocet_umrti(int) F| kumulativni_pocet_testu(int) F| kumulativni_pocet_ag_testu(int) F|
    prirustkovy_pocet_nakazenych(int) F| prirustkovy_pocet_vylecenych(int) F| prirustkovy_pocet_umrti(int) F| prirustkovy_pocet_provedenych_testu(int) F| prirustkovy_pocet_provedenych_ag_testu(int) F
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    print("===========================================" * 3)
    print("Saving group_1 to influx database covid-19 ....")
    print("===========================================" * 3)
    # hospitalizace
    # -------------
    downloaded_data = download_csv_data(urls["hospitalizace"])

    measurement = "group_1-hospitalizace"

    unwanted_columnts = ["id", "pacient_prvni_zaznam", "hfno", "upv", "ecmo", "tezky_upv_ecmo", "kum_pacient_prvni_zaznam"]
    hosp_data_for_db = prepare_data_for_db(measurement, downloaded_data, unwanted_columnts)
    show_schema(hosp_data_for_db)
    save_data_to_db(dbclient, hosp_data_for_db)

    # nakazeni-vyleceni-umrti-testy
    # -----------------------------
    downloaded_data = download_csv_data(urls["nakazeni-vyleceni-umrti-testy"])

    nakaz_measurement = "group_1-nakazeni-vyleceni-umrti-testy"

    nakaz_data_for_db = prepare_data_for_db(nakaz_measurement, downloaded_data)
    show_schema(nakaz_data_for_db)
    save_data_to_db(dbclient, nakaz_data_for_db)


def save_group_2_to_db(dbclient, urls):
    """Save group_2 to influx database.

    column name(data type) SAVED_AS
    SAVED_AS -> T-tag, F-field, TM-time

    Save `kraj-okres-nakazeni-vyleceni-umrti.csv`:
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    datum(date) TM| kraj_nuts_kod(str) T| okres_lau_kod(str) T| kumulativni_pocet_nakazenych(int) F| kumulativni_pocet_vylecenych(int) F| kumulativni_pocet_umrti(int) F
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Save `obyvatelstvo.csv`: no time series -> using idhod filed as fake timestamp
    -------------------------------------------------------------------------------------------------------------
    idhod(date) TM| hodnota(int) F| stapro_kod(int) F| pohlavi_kod(int) F| vuzemi_cis(int) T| vuzemi_kod(int) T
    -------------------------------------------------------------------------------------------------------------

    """
    print("===========================================" * 3)
    print("Saving group_2 to influx database covid-19 ....")
    print("===========================================" * 3)

    # kraj-okres-nakazeni-vyleceni-umrti
    # ----------------------------------
    downloaded_data = download_csv_data(urls["kraj-okres-nakazeni-vyleceni-umrti"])

    measurement = "group_2-kraj-okres-nakazeni-vyleceni-umrti"

    unwanted_columnts = ["id"]
    tags_columns = [("kraj_nuts_kod", str), ("okres_lau_kod", str)]
    kraj_okres_data_for_db = prepare_data_for_db(measurement, downloaded_data, unwanted_columnts, tags_columns)
    show_schema(kraj_okres_data_for_db)
    save_data_to_db(dbclient, kraj_okres_data_for_db)

    # obyvatelstvo
    # ----------------------------------
    obyv_csv_reader = download_csv_data(urls["obyvatelstvo"])

    measurement = "group_2-obyvatelstvo"

    unwanted_columnts = ["pohlavi_cis", "vek_cis", "pohlavi_txt", "vek_txt", "vuzemi_txt"]
    tags_columns = [("vuzemi_kod", int), ("pohlavi_kod", str), ("vek_kod", str)]
    date_column = "casref_do"
    obyvatelstvo_data_for_db = prepare_data_for_db(measurement, obyv_csv_reader, unwanted_columnts, tags_columns, date_column)
    show_schema(kraj_okres_data_for_db)
    save_data_to_db(dbclient, obyvatelstvo_data_for_db)


def save_group_3_to_db(dbclient, urls):
    """Save group_3 to influx database.

    column name(data type) SAVED_AS
    SAVED_AS -> T-tag, F-field, TM-time

    Save `ockovani-umrti.csv`:
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    TODO description
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Save `ockovani-pozitivni`:
    -------------------------------------------------------------------------------------------------------------
    TODO description
    -------------------------------------------------------------------------------------------------------------

    """
    print("===========================================" * 3)
    print("Saving group_3 to influx database covid-19 ....")
    print("===========================================" * 3)

    # ockovani-umrti
    # ----------------------------------
    downloaded_data = download_csv_data(urls["ockovani-umrti"])

    measurement = "group_3-ockovani-umrti"

    unwanted_columnts = [
        "id", "zemreli_bez_ockovani_relativni_pocet", "zemreli_nedokoncene_ockovani_vek_prumer",
        "zemreli_dokoncene_ockovani_relativni_pocet", "zemreli_dokoncene_ockovani_vek_prumer", "zemreli_posilujici_davka_vek_prumer"
        ]
    umrti_data_for_db = prepare_data_for_db(measurement, downloaded_data, unwanted_columnts)
    show_schema(umrti_data_for_db)
    save_data_to_db(dbclient, umrti_data_for_db)

    # ockovani-pozitivni
    # ----------------------------------
    downloaded_data = download_csv_data(urls["ockovani-hospitalizace"])

    measurement = "group_3-ockovani-hospitalizace"

    unwanted_columnts = [
        "id", "hospitalizovani_bez_ockovani_relativni_pocet", "hospitalizovani_nedokoncene_ockovani_relativni_pocet",
        "hospitalizovani_nedokoncene_ockovani_vek_prumer", "hospitalizovani_dokoncene_ockovani_relativni_pocet", "hospitalizovani_dokoncene_ockovani_vek_prumer",
        "hospitalizovani_posilujici_davka","hospitalizovani_posilujici_davka_relativni_pocet","hospitalizovani_posilujici_davka_vek_prumer"
    ]
    pozitivni_data_for_db = prepare_data_for_db(measurement, downloaded_data)
    show_schema(pozitivni_data_for_db)
    save_data_to_db(dbclient, pozitivni_data_for_db)


def save_group_4_to_db(dbclient, urls):
    """Save group_4 to influx database.

    column name(data type) SAVED_AS
    SAVED_AS -> T-tag, F-field, TM-time

    Save `kraj-okres-testy.csv`:
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    TODO description
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    print("===========================================" * 3)
    print("Saving group_4 to influx database covid-19 ....")
    print("===========================================" * 3)

    # kraj-okres-testy
    # ----------------------------------
    downloaded_data = download_csv_data(urls["kraj-okres-testy"])

    measurement = "group_4-kraj-okres-testy"

    tags_columns = [("kraj_nuts_kod", str), ("okres_lau_kod", str)]
    testy_data_for_db = prepare_data_for_db(measurement, downloaded_data, tags_columns=tags_columns)
    show_schema(testy_data_for_db)
    save_data_to_db(dbclient, testy_data_for_db)


def save_group_5_to_db(dbclient, urls):
    """Save group_5 to influx database.

    column name(data type) SAVED_AS
    SAVED_AS -> T-tag, F-field, TM-time

    Save `ockovani.csv`:
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    TODO description
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    Save `osoby.csv`:
    ---------------------------------------------------------------------------------------------------------------------------------------------------------------------
    TODO description
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    """
    print("===========================================" * 3)
    print("Saving group_5 to influx database covid-19 ....")
    print("===========================================" * 3)

    # ockovani
    # ----------------------------------
    downloaded_data = download_csv_data(urls["ockovani"])

    measurement = "group_5-ockovani"
    tags_columns = [("kraj_nuts_kod", str), ("vekova_skupina", str), ("vakcina", str)]
    ockovani_data_for_db = prepare_data_for_db(measurement, downloaded_data, tags_columns=tags_columns)
    show_schema(ockovani_data_for_db)
    save_data_to_db(dbclient, ockovani_data_for_db)

    # osoby
    # ----------------------------------
    downloaded_data = download_csv_data(urls["osoby"])

    measurement = "group_5-osoby"

    unwanted_colums = ["nakaza_zeme_csu_kod", "reportovano_khs", "nakaza_v_zahranici"]
    tags_columns = [("kraj_nuts_kod", str), ("okres_lau_kod", str)]
    osoby_data_for_db = prepare_data_for_db(measurement, downloaded_data, unwanted_columnts=unwanted_colums, tags_columns=tags_columns, now=True)
    show_schema(osoby_data_for_db)
    print(len(osoby_data_for_db))
    save_data_to_db(dbclient, osoby_data_for_db)
