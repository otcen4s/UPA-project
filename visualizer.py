#!/usr/bin/env python

from scraper_funcs import connect_to_db, create_and_switch_to_db
from xkubik32 import task_a_1, task_a_2
from b_queries import task1, task2


def main():
    upa_proj_db = "covid-19"
    client = connect_to_db()
    create_and_switch_to_db(client, upa_proj_db)


    task1(client)
    task2(client)
    #task_a_1(client)
    #task_a_2(client)


if __name__ == "__main__":
    main()
