from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import urllib2
import json

"""
Sample:

    {"county_name":"Statewide",
    "date":"2004-01-01T00:00:00.000",
    "snap_dollars":"74577052.00",
    "snap_individuals":"914902",}


Transformations:
* Turn date YYYY-MM-DD
"""

DATA_FILE_PATH = 'data/snap.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a pandas DataFrame.
    """
    URL = 'http://data.pa.gov/resource/vjq8-nahv.json'
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

        print(datum["snap_dollars"])
        snap_dollars = float(datum["snap_dollars"])
        snap_individuals = int(datum["snap_individuals"])


        data_point = {
            'county': county,
            'date': date,
            'snap_dollars': snap_dollars,
            'snap_individuals': snap_individuals}

        data_points.append(data_point)

    return data_points

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'kd9x-cq7y',
        'name': 'Supplemental Nutrition Assistance Program Individuals And Dollars 2004 - Current Human ServicesHuman Services Medical Assistance Enrollment July 2003 - Current Human Services',
        'categories': ['Human Services'],
        'tags': ['nutrition,snap,human,service,federal,individual,dollar,assistance,food,stamps'],
        'measures': ['snap_dollars','snap_individuals'],
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
