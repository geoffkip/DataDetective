from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import json
import csv
"""
Sample:
TCount,Textbox1,TRatePercent,Geography,Calendar_Year,DT_COUNT,DT_DENOM,DT_RATE,DT_LB,DT_UB1	Significance	County_Code


Transformations:

"""

DATA_FILE_PATH = 'data/low_birth_weight.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a pandas DataFrame.
    """
    f = open('data/eddi/low_birth_weight.csv', 'r')
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
    low_birth_weight = []
    for datum in data:
        print(datum)
        county = datum["Geography"]
        year = datum["Calendar_Year"]
        low_weight_births = int(datum["DT_COUNT"].replace(',',''))
        total_births = int(datum["DT_DENOM"].replace(',',''))

        data_point = {
            'county': county,
            'date': year+'-01-01',
            'low_weight_births': low_weight_births,
            'total_births': total_births}

        low_birth_weight.append(data_point)

    low_birth_weight_dataframe = pd.DataFrame.from_dict(low_birth_weight)
    #print(hospitalizations_dataframe.head (10))

    return low_birth_weight_dataframe.T.to_dict().values()

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'aps5-fttf',
        'measures': ['low_weight_births','total_births'],
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
