from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import urllib2
import json

"""
Sample:
{
    "county":"Erie",
    "corrections_population":"2,274",
    "date":"11-2015",
}
"""

DATA_FILE_PATH = 'data/corrections_pop.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a dictionary.
    """
    URL = 'http://data.pa.gov/resource/efrh-6mcn.json'

    # Get JSON data from the URL
    response = urllib2.urlopen(URL)
    extracted_data  = json.load(response)

    return extracted_data

def transform(data):
    """
    Parses extracted_data into a list of dictionaries of the DataPoint form:
        county: string
        date: string (MM-YYYY)
        measure_1: Number
        measure_2: Number
        ...
        measure_n: Number
    """
    data_points = []
    finished = []
    county_data_set = []

    for datum in data:
        full_date = datum['date'].split("-")
        month = full_date[1] + "-" + full_date[0]
        institution = datum['institution']
        county_datum = {
            "corrections_population": int(datum['corrections_population']),
            "county": datum['county'],
            "month": month,
            "institution": datum['institution']
        }
        county_data_set.append(county_datum)


    #pprint(county_data_set)

    correction_dataframe = pd.DataFrame.from_dict(county_data_set)
    # Group by month, take the max for each institution
    # Group by county, sum them
    print(correction_dataframe.head(10))
    agg_function_max = {'corrections_population': ['max']}
    correction_dataframe = correction_dataframe.groupby(["county", "institution", "month"]).agg(agg_function_max)
    correction_dataframe.reset_index(inplace=True)
    correction_dataframe.columns = pd.Index(['county','institution','month','corrections_population'])
    print(correction_dataframe.head(10))
    print(correction_dataframe.columns)
    agg_function_sum = {'corrections_population': ['sum']}
    correction_dataframe = correction_dataframe.groupby(["county", "month"]).agg(agg_function_sum)

    pprint(correction_dataframe)
    correction_dataframe.reset_index(inplace=True)
    print(correction_dataframe.columns)
    correction_dataframe.columns = pd.Index(['county','date','corrections_population'])
    pprint(correction_dataframe)
    return correction_dataframe

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'a8qx-qnix',
        'name': 'State Correction Population June 2015 - Current, Corrections',
        'categories': ['demographics','public safety','education'],
        'tags': ['population','re-entry','public safety','corrections','doc'],
        'measures': ['corrections_population'],
        'data': records.T.to_dict().values()
    }

    with open(DATA_FILE_PATH, 'w') as data_file:
        data_file.write(json.dumps(document))

    return document


data = extract()
data_points = transform(data)
document = load(data_points)
pprint(document)
