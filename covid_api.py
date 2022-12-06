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

def create_covid_tables(cur, conn):
    cur.execute("DROP TABLE IF EXISTS Covid_Total_Cases")
    cur.execute("DROP TABLE IF EXISTS Covid_New_Cases")
    cur.execute('CREATE TABLE IF NOT EXISTS Covid_Total_Cases (country TEXT, date DATE, total_cases INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS Covid_New_Cases (country TEXT, date DATE, new_cases INTEGER)')
    conn.commit()

def open_api(c):
    # how to add each country
    country = c
    api_url = 'https://api.api-ninjas.com/v1/covid19?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': 'Gruh2y4A7/nP5iIYFcaXkQ==wmzHbb5CFhE44cbZ'}).text
    data = json.loads(response)
    return data

def add_cases_total(data, cur, conn):
    for item in data:
        country = item['country']
        # not sure about the date
        for i in item['cases']:
            # if i contains 2020 and 2021
            date = i
            total_cases = item['cases'][i]['total']
            cur.execute('INSERT  OR IGNORE INTO Covid_Total_Cases (country, date, total_cases) VALUES (?,?,?)', (country, date, total_cases))
        cur.execute('INSERT  OR IGNORE INTO Covid_Total_Cases (country, date, total_cases) VALUES (?,?,?)', (country, date, total_cases))
    conn.commit()


def add_cases_new(data, cur, conn):
    for item in data:
        country = item['country']
        for i in item['cases']:
            # if i contains 2020 and 2021 change it to just the year if not continue
            date = i
            new_cases = item['cases'][i]['new']
            cur.execute('INSERT INTO Covid_New_Cases (country, date, new_cases) VALUES (?,?,?)', (country, date, new_cases))
        cur.execute('INSERT INTO Covid_New_Cases (country, date, new_cases) VALUES (?,?,?)', (country, date, new_cases))
    conn.commit()

class TestCovidApi(unittest.TestCase):
    pass

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('api_data.db')
    country_lst = ['afghanistan', 'argentina', 'australia', 'belgium', 'brazil']
    create_covid_tables(cur, conn)

    for c in country_lst:
        data = open_api(c)
        add_cases_total(data, cur, conn)
        add_cases_new(data, cur, conn)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)


