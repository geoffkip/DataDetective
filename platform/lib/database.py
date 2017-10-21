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


def format_chart_data(datum):
    print(datum)
    # Convert to a list
    chart_data= list(datum)
    # Convert the [1] into a float
    chart_data[1]= float(chart_data[1])
    return chart_data


def get_measure_data(measure, year, month):
    """
    Returns the data for a given measure

    {
      "data": [
        ['County 1', 100],
        ['County 2', 100],
        ...
        ['County n', 100]
      ],
      "name": 'Measure Name'
    }
    """
    
    data = query("SELECT county, %s FROM data_points where year= %s and month= %s and %s is not null"
                 % (measure, year, month, measure))
    
    chart_data = map(format_chart_data,data)

    return {"data" : chart_data, "name" : measure}

