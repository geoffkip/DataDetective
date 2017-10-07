from datetime import datetime
from pprint import pprint
import pandas as pd
import numpy as np
import urllib2
import json

"""
Sample:
{
    "count":"1",
    "program_year":"PY 2013-2014",
    "training_type":"Total, All Trainings",
    "wage_1_year_change":"0.0811",
    "worker_id":"0",
    "workforce_board_name":"Statewide",
    "year_end":"2014-06-30T00:00:00.000"
}

Transformations:
* Map Workforce Center to County
* Sum the number of workers trained by county
* Average the wage_1_year_change

"""

DATA_FILE_PATH = 'data/trainings.json'

WORKFORCE_COUNTY = {
    'Northwest Workforce Investment Board': ['Erie', 'Warren', 'Crawford', 'Venango', 'Forest', 'Clarion'],
    'North Central Workforce Investment Board': ['McKean', 'Potter', 'Elk', 'Cameron', 'Jefferson', 'Clearfield'],
    'Southwest Corner Workforce Investment Board': ['Beaver', 'Washington', 'Greene'],
    'Luzerne/Schuylkill Counties Workforce Investment Board': ['Luzerne', 'Schuylkill'],
    'Tri-County Workforce Investment Board': ['Butler', 'Armstrong', 'Indiana'],
    'Pocono Counties Workforce Investment Board': ['Wayne', 'Pike', 'Monroe', 'Carbon'],
    'Berks County Workforce Investment Board': ['Berks'],
    'Three Rivers Workforce Investment Board': ['Allegheny'],
    'Philadelphia Workforce Investment Board': ['Philadelphia'],
    'Northern Tier Workforce Investment Board': ['Tioga', 'Bradford', 'Susquehanna', 'Sullivan', 'Wyoming'],
    'Chester County Workforce Investment Board': ['Chester'],
    'Central Pennsylvania Workforce Investment Board': ['Centre', 'Clinton', 'Mifflin', 'Union', 'Snyder', 'Lycoming', 'Columbia', 'Montour', 'Northhumberland'],
    'South Central Workforce Investment Board': ['Junita', 'Perry', 'Cumberland', 'Franklin', 'Adams', 'York', 'Dauphin', 'Lebanon'],
    'Lehigh Valley Workforce Investment Board': ['Leigh', 'Northhampton'],
    'Delaware County Workforce Investment Board': ['Delaware'],
    'West Central Workforce Investment Board': ['Mercer', 'Lawrence'],
    'Westmoreland/Fayette Workforce Investment Board': ['Westmoreland', 'Fayette'],
    'Lancaster County Workforce Investment Board': ['Lancaster'],
    'Statewide': ['N/A']
}

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a pandas DataFrame.
    """
    URL = 'http://data.pa.gov/resource/gqf2-rjtp.json'
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
    county_data_set = []

    # Step 1: Map to county, build a new dataset
    for datum in data:
        for county in WORKFORCE_COUNTY[datum['workforce_board_name']]:
            county_datum = {
                "count": int(datum['count']),
                # NOTE: We don't need this since we'll aggregate them out
                #"program_year": datum['program_year'],
                #"training_type": datum['training_type'],
                "wage_1_year_change": float(datum['wage_1_year_change']),
                "county": county,
                "year_end": datum['year_end']
            }
            county_data_set.append(county_datum)

    pprint(county_data_set)

    # Step 2: Aggregate by county, sum(count), avg(wage_1_year_change)
    training_dataframe = pd.DataFrame.from_dict(county_data_set)
    agg_function = {'count': ['sum'], 'wage_1_year_change': [np.mean] }
    training_dataframe = training_dataframe.groupby(["county", "year_end"]).agg(agg_function)

    pprint(training_dataframe)
    writer = pd.ExcelWriter('data/WDA_performance_2014.xlsx')
    training_dataframe.to_excel(writer,'2014')
    writer.save()


    # for datum in data:
    #     county =
    #     date =
    #     trainings  =
    #     average_wage_change =
    #
    #     data_point = {
    #         'county': county,
    #         'date': date.strftime('%Y-%m-%d'),
    #         'trainings': trainings,
    #         'average_wage_change': average_wage_change
    #     }
    #
    #     data_points.append(data_point)
    #
    # return data_points

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'd5pf-ti7w',
        'name': 'All Jobs January 2015 To October 2016 Community and Economic Development',
        'categories': ['economy','social services'],
        'tags': ['community','dced','jobs','job','economic'],
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
