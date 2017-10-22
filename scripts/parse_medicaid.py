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
    URL = 'http://data.pa.gov/api/views/2ght-hfn9/rows.json'
    response = urllib2.urlopen(URL)
    extracted_data  = json.load(response)

    return extracted_data["data"]

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

        county                      = datum[16]
        date                        = datum[13][0:10]
        ma_children = int(datum[17])
        ma_individuals = int(datum[18])

        data_point = {
            'county': county,
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
        'categories': ['social services','finance','health'],
        'tags': ['assistance','medical','insurance','medicaid','ma','dhs','enroll','health'],
        'measures': ['ma_children','ma_individuals'],
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
