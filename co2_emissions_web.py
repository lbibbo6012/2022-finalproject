import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup


# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_co2_table(cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS CO2_Emissions (country_id INTEGER, emissions_2020 NUMBER, emissions_2021 NUMBER)')
    conn.commit()

# Change 
def addEmissionsData(countries_lst, id, soup, cur, conn):
    table = soup.find('table', class_='ecl-table ecl-table--zebra')
    rows = table.find_all('tr', class_='ecl-table__row')
    for row in rows:
        line = row.find_all('td')
        row_ind = [i.text for i in line]

        if len(row_ind) > 0:
            country = row_ind[0].lower()

            if country in countries_lst:
                emissions_2020 = row_ind[6]
                emissions_2021 = row_ind[7]
                cur.execute('INSERT INTO CO2_Emissions (country_id, emissions_2020, emissions_2021) VALUES (?,?,?)', (id, emissions_2020, emissions_2021))
                conn.commit()

class TestCO2Emissions(unittest.TestCase):
    pass

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('api_data.db')
    create_co2_table(cur, conn)

    url = 'https://edgar.jrc.ec.europa.eu/report_2022'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    countries_lst = ['china','united states', 'india', 'russia', 'iran', 'germany', 'indonesia', 'saudi arabia', 'canada',
    'brazil', 'south africa', 'mexico', 'australia', 'united kingdom', 'vietnam', 'poland', 'thailand', 'egypt',
    'malaysia', 'pakistan', 'kazakhstan', 'united arab emirates', 'argentina', 'ukraine', 'iraq', 'algeria', 'philippines', 'netherlands',
    'nigeria', 'uzbekistan', 'bangladesh', 'venezuela', 'kuwait', 'czechia', 'qatar', 'belgium', 'oman', 'chile', 'romania', 'colombia', 
    'morocco', 'austria', 'libya', 'belarus', 'singapore', 'peru', 'greece', 'hungary', 'bulgaria', 'norway', 'ecuador', 'finland', 'sweden', 
    'portugal', 'bahrain', 'slovakia', 'azerbaijan', 'ireland', 'new zealand', 'tunisia', 'dominican republic', 'denmark', 'syria', 'lebanon', 
    'mongolia', 'cuba', 'angola', 'jordan', 'sri lanka', 'ghana', 'bolivia', 'kenya', 'laos', 'guatemala', 'ethiopia', 'croatia', 'cambodia',
    'estonia', 'nepal', 'lithuania', 'tanzania', 'panama', 'zimbabwe', 'yemen', 'senegal', 'georgia', 'cameroon', 
    'tajikistan', 'honduras', 'moldova', 'paraguay', 'mozambique', 'benin', 'luxembourg', 'afganistan', 'el salvador', 'costa rica', 'jamaica',
    'congo', 'brunei', 'latvia', 'zambia', 'botswana', 'uganda', 'uruguay', 'armenia'
    ]

    countries_lst.sort()
    
    cur.execute('SELECT max(country_id) FROM CO2_Emissions')
    min = cur.fetchone()[0]
    if type(min) != int:
        min = 0
    id = min + 1

    for i in range(min, min + 10):
        addEmissionsData(countries_lst[i], id, soup, cur, conn)
        id = id + 1

    conn.close()
    

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)


