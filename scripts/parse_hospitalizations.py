from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import json
import csv
"""
Sample:
TRatePercent,Health_Events,Geography,CalendarYear,Gender,RaceEthnicity,Textbox3,DT_Count,DT_Population,DT_RATE,DT_LB,DT_UB1,Significance,County_Code
   Age-Adjusted Rate,Asthma,Pennsylvania,2014,Total,All Races,All ages,"17,417","12,793,767",13.4,13.2,13.6,,000


Transformations:

"""

DATA_FILE_PATH = 'data/hospitalization.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a pandas DataFrame.
    """
    f = open('data/eddi/Hospitalization.csv', 'r')
    reader = csv.DictReader(f)
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
    hospitalizations = []
    for datum in data:
        county = datum["Geography"]
        year = datum["CalendarYear"]
        health_events = datum["Health_Events"]
        gender = datum["Gender"]
        ethnicity = datum["RaceEthnicity"]
        age = datum["Textbox3"]
        try:
            total_population = int(datum["DT_Population"].replace(',',''))
        except ValueError as e:
            total_population = 0
        try:
            count = int(datum["DT_Count"].replace(',',''))
        except ValueError as e:
            count = 0

        data_point = {
            'county': county,
            'date': year+'-01-01',
            'health_events': health_events,
            'gender': gender,
            'ethnicity': ethnicity,
            'age': age,
            'total_population_asthma': total_population,
            'count_asthma_hospitalizations': count}

        hospitalizations.append(data_point)

    hospitalizations_dataframe = pd.DataFrame.from_dict(hospitalizations)

    agg_function_max = {'total_population_asthma': ['sum'],'count_asthma_hospitalizations': ['sum']}
    hospitalizations_dataframe = hospitalizations_dataframe.groupby(["county","date"]).agg(agg_function_max)

    hospitalizations_dataframe.reset_index(inplace=True)
    hospitalizations_dataframe.columns = pd.Index (['county', 'date', 'total_population_asthma', 'count_asthma_hospitalizations'])
    return hospitalizations_dataframe.T.to_dict().values()


def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'aps5-fttf',
        'name': 'Enterprise Data Dissemination Informatics Exchange Department of Health: Hospitalizations by County 2001-2014',
        'categories': ['social services','finance','health'],
        'tags': ['statistics', 'health', 'informatics', 'exchange', 'air', 'disease', 'hospital'],
        'measures': ['total_population_asthma', 'count_asthma_hospitalizations'],
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
