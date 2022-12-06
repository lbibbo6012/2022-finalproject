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
    cur.execute("DROP TABLE IF EXISTS CO2_Emissions")
    cur.execute('CREATE TABLE IF NOT EXISTS CO2_Emissions (country TEXT, year INTEGER, total_cases INTEGER)')
    conn.commit()

# Change 
def getEmissionsData(soup):
    d = {}
    div = soup.find('div', class_='wp-block-column')
    table = soup.find()
    for row in table.find_all('tr'):
        line = row.find_all('td')
        print(line)
        d[line[0].text.replace('\\n', '').strip()] = line[1].text.replace('\\n', '').strip()
    return d


class TestCO2Emissions(unittest.TestCase):
    pass

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('api_data.db')

    url = 'https://ourworldindata.org/co2-emissions'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #Call the functions getLink(soup) and getAdmissionsInfo2019(soup) on your soup object.
    getEmissionsData(soup)


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
