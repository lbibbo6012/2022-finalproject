import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def create_co2_table(cur, conn):
    cur.execute("DROP TABLE IF EXISTS CO2_Emissions")
    cur.execute('CREATE TABLE IF NOT EXISTS CO2_Emissions (country TEXT, emissions_2020 NUMBER, emissions_2021 NUMBER)')
    conn.commit()

# Change 
def addEmissionsData(soup, cur, conn):
    table = soup.find('table', class_='ecl-table ecl-table--zebra')
    rows = table.find_all('tr', class_='ecl-table__row')
    for row in rows:
        line = row.find_all('td')
        row_ind = [i.text for i in line]

        if len(row_ind) > 0:
            country = row_ind[0].lower()
            # ask about hardcoding
            emissions_2020 = row_ind[6]
            emissions_2021 = row_ind[7]
            cur.execute('INSERT INTO CO2_Emissions (country, emissions_2020, emissions_2021) VALUES (?,?,?)', (country, emissions_2020, emissions_2021))
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

    #Call the functions getLink(soup) and getAdmissionsInfo2019(soup) on your soup object.
    addEmissionsData(soup, cur, conn)


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

