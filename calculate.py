import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
# starter code

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def data_calc(cur, conn):
    data = {}
    lst = []
    cur.execute('SELECT Country_IDs.country, Covid_Cases.cases_feb_01_2020, Covid_Cases.cases_feb_01_2021, CO2_Emissions.emissions_2020, CO2_Emissions.emissions_2021 FROM Country_IDs JOIN Covid_Cases ON Country_IDs.country_id = Covid_Cases.country_id JOIN CO2_Emissions ON CO2_Emissions.country = Country_IDs.country')
    
    lst = cur.fetchall()
    for item in lst:
        print(item)
        data[item[0]] = {}
        data[item[0]]['cases_difference'] = round((item[2] - item[1]), 2)
        data[item[0]]['emissions_difference'] = round((item[4] - item[3]), 2)
    
    return data

# add in a ratio calculation

def double_bar_vis(data):
    country_lst = []
    emissions_lst = []
    covid_cases_lst = []
    for item in data:
        country_lst.append(item)
    
    for country in country_lst:
        covid_cases_lst.append(data[country]['cases_difference'])
    
    for country in country_lst:
        emissions_lst.append(data[country]['emissions_difference'])
    
    fig = go.Figure(data = )
    
    

def main():
    cur, conn = setUpDatabase('api_data.db')
    data = data_calc(cur, conn)
    double_bar_vis(data)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
