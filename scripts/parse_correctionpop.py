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
    "date":"2014-2015",
}
"""

DATA_FILE_PATH = 'corrections_pop.json'



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
        date: string (YYYY-YYYY)
        measure_1: Number
        measure_2: Number
        ...
        measure_n: Number
    """
    data_points = []
    finished = []
    county_data_set = []

    for datum in data:
        full_date = datum['fiscal_year'].split(" ")
        year = full_date[1]
        institution = datum['institution']
        if not([institution, year] in finished):
            county_datum = {
                "corrections_population": int(datum['corrections_population']),
                "county": datum['county'],
                "fiscal_year": year
            }
            county_data_set.append(county_datum)
        finished.append([institution, year])

    #pprint(county_data_set)

    correction_dataframe = pd.DataFrame.from_dict(county_data_set)
    agg_function = {'corrections_population': ['sum']}
    correction_dataframe = correction_dataframe.groupby(["county", "fiscal_year"]).agg(agg_function)

    #pprint(correction_dataframe)

    return correction_dataframe



    """
    for datum in data:
        #print (resource.keys())
        county                      = datum["county"]
        year = datum["fiscal_year"]


        if county not in counties:
            counties.append(county)
        if year not in years:
            years.append(year)

    for county in counties:
        for year in years:
            pop_sum = 0
            for datum in data:
                if county == datum["county"]:
                    if year == datum["fiscal_year"]:
                        pop_sum += int(datum["corrections_population"])
                        full_date = datum["fiscal_year"].split(" ")
                        date                        = full_date[1]

            data_point = {
                'county': county,
                'date': date,
                'corrections_population': pop_sum
                }

            data_points.append(data_point)

    return data_points
"""
def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'a8qx-qnix',
        'name': 'State Correction Population June 2015 - Current, Corrections',
        'categories': ['demographics','public safety','education'],
        'tags': ['population','re-entry','public safety','corrections','doc'],
        'data': records
    }

    with open(DATA_FILE_PATH, 'w') as data_file:
        data_file.write(json.dumps(document))




    return document


data = extract()
data_points = transform(data)
document = load(data_points)
pprint(document)
