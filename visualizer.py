#!/usr/bin/env python


from scraper_funcs import connect_to_db, create_and_switch_to_db


from queries_task2 import task1
from xkubik32 import task_1


def main():
    upa_proj_db = "covid-19"
    client = connect_to_db()
    create_and_switch_to_db(client, upa_proj_db)

    task_1(client)


if __name__ == "__main__":
    main()
