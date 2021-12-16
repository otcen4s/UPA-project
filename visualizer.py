#!/usr/bin/env python

from scraper_funcs import connect_to_db, create_and_switch_to_db
from xkubik32 import task_a_1, task_a_2
from b_queries import task1, task2
from xkacur04_task1 import task1 as xkacur04_task1
from xkacur04_task2 import task2 as xkacur04_task2


def main():
    upa_proj_db = "covid-19"
    client = connect_to_db()
    create_and_switch_to_db(client, upa_proj_db)

    # xkubik32
    task_a_1(client)
    task_a_2(client)

    # xotcen01
    task1(client)
    task2(client)

    # xkacur04
    xkacur04_task1(client)
    xkacur04_task2(client)


if __name__ == "__main__":
    main()
