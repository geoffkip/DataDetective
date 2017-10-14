from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import json
import csv
"""
Sample:
CountyState,Calendar_Year,Poverty_LT5,Pct_Poverty_LT5,FIPSCode


Transformations:

"""

DATA_FILE_PATH = 'data/poverty.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a pandas DataFrame.
    """
    f = open('data/poverty.csv', 'r')
    reader = csv.DictReader(f,delimiter='\t')
    extracted_data = [row for row in reader]

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
    poverty = []
    for datum in data:
        print(datum)
        county = datum["CountyState"]
        year = datum["Calendar_Year"]
        children_in_poverty = int(datum["Poverty_LT5"].replace(',',''))
        percent_children_in_poverty = float(datum["Pct_Poverty_LT5"])


        data_point = {
            'county': county,
            'date': year+'-01-01',
            'children_in_poverty': children_in_poverty,
            'percent_children_in_poverty': percent_children_in_poverty,
            }

        poverty.append(data_point)

    poverty_dataframe = pd.DataFrame.from_dict(poverty)
    #print(hospitalizations_dataframe.head (10))

    return poverty_dataframe.T.to_dict().values()

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'aps5-fttf',
        'name': 'Enterprise Data Dissemination Informatics Exchange Department of Health: Hospitalizations by County 2001-2014',
        'categories': ['social services,finance,health'],
        'tags': ['statistics', 'health', 'informatics', 'exchange', 'child', 'cancer', 'birth', 'air', 'disease', 'hospital', 'housing', 'pregnancies'],
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
