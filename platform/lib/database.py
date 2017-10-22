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

county_fips_codes = {
        "Butler" : "us-pa-019",
        "Greene" : "us-pa-059",
        "Adams" : "us-pa-001",
        "Jefferson" : "us-pa-065",
        "Potter" : "us-pa-105",
        "Fayette" : "us-pa-051",
        "Lycoming" : "us-pa-081",
        "Union" : "us-pa-119",
        "Venango" : "us-pa-121",
        "Lebanon" : "us-pa-075",
        "Montgomery" : "us-pa-091",
        "Somerset" : "us-pa-111",
        "Delaware" : "us-pa-045",
        "Mercer" : "us-pa-085",
        "Northampton" : "us-pa-095",
        "Forest" : "us-pa-053",
        "Westmoreland" : "us-pa-129",
        "Allegheny" : "us-pa-003",
        "Cameron" : "us-pa-023",
        "York" : "us-pa-133",
        "Centre" : "us-pa-027",
        "Fulton" : "us-pa-057",
        "Pike" : "us-pa-103",
        "Carbon" : "us-pa-025",
        "Huntingdon" : "us-pa-061",
        "Washington" : "us-pa-125",
        "Warren" : "us-pa-123",
        "Lackawanna" : "us-pa-069",
        "Crawford" : "us-pa-039",
        "Bradford" : "us-pa-015",
        "Cambria" : "us-pa-021",
        "Mifflin" : "us-pa-087",
        "Schuylkill" : "us-pa-107",
        "Franklin" : "us-pa-055",
        "Chester" : "us-pa-029",
        "Columbia" : "us-pa-037",
        "Dauphin" : "us-pa-043",
        "Berks" : "us-pa-011",
        "Susquehanna" : "us-pa-115",
        "Bucks" : "us-pa-017",
        "McKean" : "us-pa-083",
        "Philadelphia" : "us-pa-101",
        "Sullivan" : "us-pa-113",
        "Cumberland" : "us-pa-041",
        "Wayne" : "us-pa-127",
        "Beaver" : "us-pa-007",
        "Elk" : "us-pa-047",
        "Juniata" : "us-pa-067",
        "Northumberland" : "us-pa-097",
        "Snyder" : "us-pa-109",
        "Tioga" : "us-pa-117",
        "Luzerne" : "us-pa-079",
        "Erie" : "us-pa-049",
        "Bedford" : "us-pa-009",
        "Indiana" : "us-pa-063",
        "Lawrence" : "us-pa-073",
        "Clearfield" : "us-pa-033",
        "Monroe" : "us-pa-089",
        "Lancaster" : "us-pa-071",
        "Perry" : "us-pa-099",
        "Wyoming" : "us-pa-131",
        "Blair" : "us-pa-013",
        "Montour" : "us-pa-093",
        "Armstrong" : "us-pa-005",
        "Lehigh" : "us-pa-077",
        "Clarion" : "us-pa-031",
        "Clinton" : "us-pa-035"
        }

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

def format_geo_chart_data(datum):
    print(datum)
    # Convert to a list
    chart_data= list(datum)
    # Convert the [1] into a float
    chart_data[1]= float(chart_data[1])
    chart_data[0]= county_fips_codes[chart_data[0]]

    return chart_data

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


# TODO: Build get_measure_data(measure, year, format='timeseries')
# TODO: Build get_measure_data(measure, year, format='geo')
# TODO: Build get_measure_data(measure, year, format='column')
def get_measure_data(measure, year, month, chart="column"):
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
    _query = "SELECT county, %s FROM data_points where year= %s and %s is not null and county not in ('Pennsylvania','Statewide','N/A','Statewide Project')" % (measure, year, measure)
    data = query(_query)

    if chart == "column":
        chart_data = map(format_chart_data,data)

    if chart == "geo":
        chart_data= map(format_geo_chart_data,data)

    return {"data" : chart_data, "name" : measure}
