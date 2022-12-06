import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_tables(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Covid_Cases")
    cur.execute("DROP TABLE IF EXISTS Country_IDs")
    cur.execute('CREATE TABLE IF NOT EXISTS Country_IDs (country_id INTEGER PRIMARY KEY, country TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Covid_Cases (country_id INTEGER, total_cases_2020 INTEGER, total_cases_2021 INTEGER)')
    conn.commit()

def open_api(c):
    # how to add each country
    country = c
    api_url = 'https://api.api-ninjas.com/v1/covid19?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': 'Gruh2y4A7/nP5iIYFcaXkQ==wmzHbb5CFhE44cbZ'}).text
    data = json.loads(response)
    return data

def add_country(data, id, cur, conn):
    for item in data:
        country = item['country']
        country_id = id
        cur.execute('INSERT OR IGNORE INTO Country_IDs (country_id, country) VALUES (?,?)', (country_id, country))
    conn.commit()

def add_cases_total(data, id, cur, conn):
    total_cases_2020 = 0
    total_cases_2021 = 0
    for item in data:
        country_id = id
        for i in item['cases']:
            if '2020-02-01' in i:
                total_cases_2020 = total_cases_2020 + item['cases'][i]['total']
            elif '2021-02-01' in i:
                total_cases_2021 = total_cases_2021 + item['cases'][i]['total']
            else:
                continue
    cur.execute('INSERT OR IGNORE INTO Covid_Cases (country_id, total_cases_2020, total_cases_2021) VALUES (?,?,?)', (country_id, total_cases_2020, total_cases_2021))
    conn.commit()


class TestCovidApi(unittest.TestCase):
    pass

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('api_data.db')
    country_lst = ['china']
    create_tables(cur, conn)
    id = 0

    for c in country_lst:
        data = open_api(c)
        add_cases_total(data, id, cur, conn)
        add_country(data, id, cur, conn)
        id = id + 1

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)


