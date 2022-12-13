import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import csv
# starter code

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


def data_calc(cur, conn):
    data = {}
    lst = []
    cur.execute('SELECT Country_IDs.country, Covid_Cases.cases_feb_01_2020, Covid_Cases.cases_feb_01_2021, CO2_Emissions.emissions_2020, CO2_Emissions.emissions_2021 FROM Country_IDs JOIN Covid_Cases ON Country_IDs.country_id = Covid_Cases.country_id JOIN CO2_Emissions ON CO2_Emissions.country_id = Country_IDs.country_id')
    
    lst = cur.fetchall()
    for item in lst:
        data[item[0]] = {}
        data[item[0]]['cases_difference'] = round(((item[2] - item[1]) / 100000), 2)
        data[item[0]]['emissions_difference'] = (round((item[4] - item[3]), 2))
    
    return data

def emissions_calc(cur, conn):
    data = {}
    lst = []
    cur.execute('SELECT Country_IDs.country, CO2_Emissions.emissions_2020, CO2_Emissions.emissions_2021 FROM Country_IDs JOIN CO2_Emissions ON CO2_Emissions.country_id = Country_IDs.country_id')
    lst = cur.fetchall()
    total_change = 0

    for item in lst:
        data[item[0]] = {}
        data[item[0]]['difference'] = round((item[2] - item[1]), 2)
    
    return data

def cases_calc(cur, conn):
    data = {}
    lst = []
    cur.execute('SELECT Country_IDs.country, Covid_Cases.cases_feb_01_2020, Covid_Cases.cases_feb_01_2021 FROM Country_IDs JOIN Covid_Cases ON Covid_Cases.country_id = Country_IDs.country_id')
    lst = cur.fetchall()
    total_change = 0


    for item in lst:
        data[item[0]] = {}
        data[item[0]]['difference'] = round((item[2] - item[1]) , 2)
    
    return data


def scatter_plot_vis(data):
    country_lst = []
    emissions_lst = []
    covid_cases_lst = []

    for item in data:
        country_lst.append(item)
    country_lst = country_lst[0:10]

    for country in country_lst:
        covid_cases_lst.append(data[country]['cases_difference'])

    for country in country_lst:
        emissions_lst.append(data[country]['emissions_difference'])

    scatter_data = {
        'Change in Covid Cases (# of cases)' : covid_cases_lst, 
        'Change in CO2 Emissions (mtons)' : emissions_lst,
        'Country' : country_lst,
        'Size' : 5,
        }
    df = pd.DataFrame(scatter_data)

    fig = px.scatter(
        df, x= 'Change in CO2 Emissions (mtons)', 
        y = 'Change in Covid Cases (# of cases)', 
        title = "February 2020 - February 2021",
        hover_data = ['Country'],
        size = 'Size'
        )

    fig.update_layout(
        font_family = 'Courier New',
        title_font_family = 'Times New Roman'
    )
    
    fig.show()

def co2_covid_vis(data):
    country_lst = []
    emissions_lst = []
    covid_cases_lst = []

    for item in data:
        country_lst.append(item)
    
    # get the top emissions for 2021
    country_lst = country_lst[0:10]
    
    for country in country_lst:
        covid_cases_lst.append(data[country]['cases_difference'])
        emissions_lst.append(data[country]['emissions_difference'])
    
    
    fig = go.Figure(data = [
        go.Bar(name = "Covid Cases Change (in 100,000 cases)", x = country_lst, y = covid_cases_lst, marker_color = 'rgb(255, 127, 80) '),
        go.Bar(name = "Emissions Change (in Mtons)", x = country_lst, y = emissions_lst, marker_color = 'rgb(100, 149, 237)')])
    fig.update_layout(barmode='group')
    fig.show()

def pie_chart(data, title):
    countries_lst = []
    percent_lst = []
    for item in data:
        countries_lst.append(item)
    
    countries_lst = countries_lst[0:10]

    for country in countries_lst:
        percent_lst.append(data[country]['difference'])

    fig = px.pie(values=percent_lst, names=countries_lst, title=title)
    fig.show()
        

def main():
    cur, conn = setUpDatabase('api_data.db')
    co2_covid_data = data_calc(cur, conn)
    co2_covid_vis(co2_covid_data)
    scatter_plot_vis(co2_covid_data)

    emissions_p_data = emissions_calc(cur, conn)
    pie_chart(emissions_p_data, 'CO2 Emissions Change by Country (as a percent of total change) Feb 2020 - Feb 2021')

    cases_p_data = cases_calc(cur,conn)
    pie_chart(cases_p_data, 'Total Covid Cases Change (as a percent of total change) by Country Feb 2020 - Feb 2021')

    small_lst = []
    all_lst = []

    for i in co2_covid_data:
        small_lst.append(i)
        small_lst.append(co2_covid_data[i]['cases_difference'])
        small_lst.append(co2_covid_data[i]['emissions_difference'])
        all_lst.append(small_lst)

        
    column_names = ['country', 'cases_difference', 'emissions_difference']

    with open('calculations.csv', 'w') as csvfile:
        write = csv.writer(csvfile)
        write.writerow(column_names)

        for i in co2_covid_data:
            small_lst = []
            small_lst.append(i)
            small_lst.append(co2_covid_data[i]['cases_difference'])
            small_lst.append(co2_covid_data[i]['emissions_difference'])
            write.writerow(small_lst)

    conn.close()

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)
