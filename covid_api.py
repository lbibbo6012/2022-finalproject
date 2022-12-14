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
    cur.execute('CREATE TABLE IF NOT EXISTS Country_IDs (country_id INTEGER PRIMARY KEY, country TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Covid_Cases (country_id INTEGER, cases_feb_01_2020 INTEGER, cases_feb_01_2021 INTEGER)')
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
        country = item['country'].lower()
        country_id = id
        cur.execute('INSERT OR IGNORE INTO Country_IDs (country_id, country) VALUES (?,?)', (country_id, country))
    conn.commit()

def add_cases_total(data, id, cur, conn):
    cases_feb_01_2020 = 0
    cases_feb_01_2021 = 0
    for item in data:
        country_id = id
        for i in item['cases']:
            if '2020-02-01' in i:
                cases_feb_01_2020  = cases_feb_01_2020 + item['cases'][i]['total']
            elif '2021-02-01' in i:
                cases_feb_01_2021 = cases_feb_01_2021 + item['cases'][i]['total']
            else:
                continue
    cur.execute('INSERT OR IGNORE INTO Covid_Cases (country_id, cases_feb_01_2020, cases_feb_01_2021) VALUES (?,?,?)', (country_id, cases_feb_01_2020, cases_feb_01_2021))
    conn.commit()


class TestCovidApi(unittest.TestCase):
    pass

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('api_data.db')
    create_tables(cur, conn)

    countries_lst = ['china','united states', 'india', 'russia', 'iran', 'germany', 'indonesia', 'saudi arabia', 'canada', 'brazil', 
    'south africa', 'mexico', 'australia', 'united kingdom', 'vietnam', 'poland', 'thailand', 'egypt', 'malaysia', 'pakistan', 
    'kazakhstan', 'united arab emirates', 'argentina', 'ukraine', 'iraq', 'algeria', 'philippines', 'netherlands','nigeria', 'uzbekistan', 
    'bangladesh', 'venezuela', 'kuwait', 'czechia', 'qatar', 'belgium', 'oman', 'chile', 'romania', 'colombia', 
    'morocco', 'austria', 'libya', 'belarus', 'singapore', 'peru', 'greece', 'hungary', 'bulgaria', 'norway', 
    'ecuador', 'finland', 'sweden', 'portugal', 'bahrain', 'slovakia', 'azerbaijan', 'ireland', 'new zealand', 'tunisia', 
    'dominican republic', 'denmark', 'syria', 'lebanon', 'mongolia', 'cuba', 'angola', 'jordan', 'sri lanka', 'ghana', 
    'bolivia', 'kenya', 'laos', 'guatemala', 'ethiopia', 'croatia', 'cambodia', 'estonia', 'nepal', 'lithuania',
    'tanzania', 'panama', 'zimbabwe', 'yemen', 'senegal', 'georgia', 'cameroon', 'tajikistan', 'honduras', 'paraguay', 
    'jamaica','madagascar','nicaragua', 'haiti', 'iceland', 'liberia', 'eritrea','somalia', 'rwanda', 'samoa'
    ]


    countries_lst.sort()
    
    cur.execute('SELECT max(country_id) FROM Covid_Cases')
    min = cur.fetchone()[0]
    if type(min) != int:
        min = 0
    id = min + 1

    for i in range(min, min + 10):
        data = open_api(countries_lst[i])
        add_cases_total(data, id, cur, conn)
        add_country(data, id, cur, conn)
        id = id + 1

    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)


