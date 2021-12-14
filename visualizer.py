#!/usr/bin/env python


from scraper_funcs import connect_to_db, create_and_switch_to_db


from queries_task2 import task1
from xkacur04_task2 import task2

def main():

     # client and DB initialization
    upa_proj_db = "covid-19"
    client = connect_to_db()
    create_and_switch_to_db(client, upa_proj_db)


    #task1(client)
    task2(client)
    
    

if __name__ == "__main__":
    main()