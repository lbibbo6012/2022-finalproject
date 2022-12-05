
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

def create_employee_table(cur, conn):
    cur.execute('')
    conn.commit()

def getLink(soup):
    olympics = soup.find('a', title='List of American universities with Olympic medals')
    url = 'https://en.wikipedia.org' + olympics.get('href')
    return url

# Change 
def getAdmissionsInfo2019(soup):
    d = {}
    table = soup.find('table', class_='toccolours')
    for row in table.find_all('tr'):
        line = row.find_all('td')
        if line[0].text != 'College/school':
            d[line[0].text.replace('\\n', '').strip()] = line[1].text.replace('\\n', '').strip()
    return d


class TestCO2Emissions(unittest.TestCase):
    pass

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('api_data.db')

    url = 'https://en.wikipedia.org/wiki/University_of_Michigan'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #Call the functions getLink(soup) and getAdmissionsInfo2019(soup) on your soup object.
    getLink(soup)


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)