from datetime import datetime
from pprint import pprint
import urllib2
import json

"""
Sample:
{
    "area_name":"Pennsylvania",
    "benchmark_year":"2016",
    "calendar_year":"2016",
    "county_code":"00",
    "county_fips":"000",
    "employed":"6120000",
    "labor_force":"6472000",
    "state_fips":"42",
    "unemployed":"352000",
    "unemployment_rate":"5.4"
}
"""

DATA_FILE_PATH = 'data/unemploment.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a dictionary.
    """
    URL = 'http://data.pa.gov/resource/raup-6gca.json'

    # Get JSON data from the URL
    response = urllib2.urlopen(URL)
    extracted_data  = json.load(response)

    return extracted_data

def transform(data):
    """
    Parses extracted_data into a list of dictionaries of the DataPoint form:
        county: string
        date: string (YYYY-MM-DD)
        measure_1: Number
        measure_2: Number
        ...
        measure_n: Number
    """
    data_points = []
    for datum in data:
        county = datum["area_name"].replace(' County', '')
        date = datum["calendar_year"]+'-01-01'
        labor_force = int(datum["labor_force"])
        unemployment_rate = float(datum["unemployment_rate"])

        data_point = {
            'county': county,
            'date': date,
            'labor_force': labor_force,
            'unemployment_rate': unemployment_rate
        }

        data_points.append(data_point)

    return data_points

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'rqq6-7e5m',
        'name': 'Local Area Unemployment Statistics 2016 Labor and Industry',
        'categories': ['Jobs that Pay'],
        'tags': ['laus', 'labor', 'employment', 'unemployment', 'force', 'dli'],
        'measures': ['labor_force', 'unemployment_rate'],
        'data': records
    }

    # TODO: Write to ElasticSearch
    with open(DATA_FILE_PATH, 'w') as data_file:
        data_file.write(json.dumps(document))

    return document

data = extract()
data_points = transform(data)
document = load(data_points)
pprint(document)
