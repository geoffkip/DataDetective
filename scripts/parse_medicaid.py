from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import urllib2
import json

"""
Sample:
{
    "[{"county_cd":"00",
    "county_name":"Statewide",
    "date":"2003-07-01T00:00:00.000",
    "ma_children":"794109",
    "ma_individuals":"1568331",
    "month_name":"July",
    "year":"2003"
}


Transformations:
* Turn date YYYY-MM-DD
"""

DATA_FILE_PATH = 'data/medicaid.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a pandas DataFrame.
    """
    URL = 'https://data.pa.gov/resource/4c6y-b2hg.json'
    response = urllib2.urlopen(URL)
    extracted_data  = json.load(response)

    return extracted_data

def transform(data):
    """
    Apply transformation to data (DataFrame).

    Returns formated data as a list of dictionaries of the DataPoint form:
        county: string
        date: string (YYYY-MM-DD)
        measure_1: Number
        measure_2: Number
        ...
        measure_n: Number
    """
    data_points = []
    for datum in data:

        county                      = datum["county_name"]
        date                        = datum["date"][0:10]
        ma_children = int(datum["ma_children"])
        ma_individuals = int(datum["ma_individuals"])
    
        data_point = {
            'county_name': county,
            'date': date,
            'ma_children': ma_children,
            'ma_individuals': ma_individuals}

        data_points.append(data_point)

    return data_points

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': '2ght-hfn9',
        'name': 'Medical Assistance Enrollment July 2003 - Current Human Services',
        'categories': ['social services,finance,health'],
        'tags': ['assistance,medical,insurance,medicaid,ma,dhs,enroll,health'],
        'data': records
    }

    # TODO: Write to ElasticSearch
    with open(DATA_FILE_PATH, 'w') as data_file:
        data_file.write(json.dumps(document))

    return document

# TODO: wrap this in an execute function
data = extract()
data_points = transform(data)
document = load(data_points)
pprint(document)
