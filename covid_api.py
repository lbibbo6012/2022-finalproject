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

def create_employee_table(cur, conn):
    cur.execute('')
    conn.commit()

def open_api():
    country ='kuwait'
    api_url = 'https://api.api-ninjas.com/v1/covid19?country={}'.format(country)
    response = requests.get(api_url, headers={'X-Api-Key': 'Gruh2y4A7/nP5iIYFcaXkQ==wmzHbb5CFhE44cbZ'}).text
    data = json.loads(response)
    return data


class TestCovidApi(unittest.TestCase):
    pass

def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('api_data.db')


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
