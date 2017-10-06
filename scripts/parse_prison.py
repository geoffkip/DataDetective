from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import urllib2
import json

"""
Sample:

{"corrections_population":"900",
"county":"N/A",
"date":"2015-08-31T00:00:00.000",
"fiscal_year":"FY 2015-2016",
"institution":"In County Jails",
"institution_type":"County Jails"}


Transformations:
* Turn date YYYY-MM-DD
"""
DATA_FILE_PATH = 'data/prisons.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a list of dictionaries.
    """
    URL = 'https://data.pa.gov/resource/efrh-6mcn.json'
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

        county                      = datum["county"]
        date                        = datum["date"][0:10]
        corrections_population  = int(datum["corrections_population"])


        data_point = {
            'county': county,
            'date': date,
            'corrections_population': corrections_population}

        data_points.append(data_point)

    return data_points

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'xmbn-f4c6',
        'name': 'State Correction Population June 2015 - Current, CorrectionsPublic Safety',
        'categories': ['Public Safety'],
        'tags': ['public safety', 're-entry', 'corrections', 'population', 'doc'],
        'data': records
    }

    # TODO: Write to ElasticSearch
    with open(DATA_FILE_PATH, 'w') as data_file:
        data_file.write(json.dumps(document))

    return document


extracted_data = extract()
data_points = transform(extracted_data)
documents = load(data_points)
