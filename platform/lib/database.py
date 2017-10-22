"""
Wrapper for PostgreSQL

Requires environmental variables be set:
    - DB_HOST
    - DB_USER
    - DB_PASSWORD
    - DB_NAME

"""
from sqlalchemy import create_engine
import psycopg2
import os
import datetime
import time

def cursor():
    """
    Returns a connection/cursor to the database
    """
    con = psycopg2.connect(host=os.environ['DB_HOST'],
                           user=os.environ['DB_USER'],
                           password=os.environ['DB_PASSWORD'],
                           database=os.environ['DB_NAME'])

    return con.cursor()

def query(sql):
    """
    Returns the results of the sql query
    """

    # TODO:
    cur= cursor()
    cur.execute(sql)
    results= cur.fetchall()

    return results

def get_measures(year):
    """
    Returns a list of measures that are available for a given year
    """
    # TODO: Select measures from database where year = year

    return measures

def format_chart_data(datum):
    chart_data= list(datum)
    chart_data[1]= float(chart_data[1])
    return chart_data

def format_timeseries_chart_data(datum):
    try:
        chart_data = []
        chart_data.append(time.mktime(datetime.datetime(datum[0],datum[1],1).utctimetuple())*1000)
        chart_data.append(float(datum[2]))
    except ValueError as e:
        print(datum)
        print(e)
    return chart_data

# TODO: Build get_measure_data(measure, year, format='timeseries')
# TODO: Build get_measure_data(measure, year, format='geo')
# TODO: Build get_measure_data(measure, year, format='column')
def get_measure_data(measure, year, month, chart='column'):
    """
    Returns the data for a given measure

    format = 'column': (county names)
        {
          "data": [
            ['County 1', 100],
            ['County 2', 100],
            ...
            ['County n', 100]
          ],
          "name": 'Measure Name'
        }
    format = 'geo': fips coded
        {
          "data": [
            ['us-pa-015', 100],
            ['us-pa-133', 100],
            ...
            ['us-pa-n', 100]
          ],
          "name": 'Measure Name'
        }
    format = 'timeseries': UTC timstamps
        {
          "data": [
            [14000000000, 100],
            [14000100000, 100],
            ...
            [n, 100]
          ],
          "name": 'Measure Name'
        }
    """
    if chart == 'timeseries':
        _query = """
                SELECT year, month, SUM({0})
                FROM data_points
                WHERE {0} is not null AND county != 'N/A'
                GROUP BY year, month
                ORDER BY year, month
                """.format(measure, year)
    else:
        _query = "SELECT county, %s FROM data_points where year= %s and %s is not null" % (measure, year, measure)

    data = query(_query)

    if chart == 'timeseries':
        chart_data = map(format_timeseries_chart_data,data)
        result = {"data" : chart_data, "name" : measure}
    else:
        chart_data = map(format_chart_data,data)
        result = {"data" : chart_data, "name" : measure}


    return result
