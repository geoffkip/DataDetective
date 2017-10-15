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
    "park_and_ride_count":"6",
    "parking_space_count":"110",
    "handicap_space_count": "8"
}
"""

DATA_FILE_PATH = 'data/park_n_ride.json'

CODE_COUNTY = {
    '1' :'Adams','2' :'Allegheny','3' :'Armstrong','4' :'Beaver','5' :'Bedford','6' :'Berks',
    '7' :'Blair','8' :'Bradford',
    '9' :'Bucks','10' :'Butler','11' :'Cambria','12' :'Cameron','13' :'Carbon','14' :'Centre',
    '15' :'Chester',
    '16' :'Clarion','17' :'Clearfield','18' :'Clinton','19' :'Columbia','20' :'Crawford',
    '21' :'Cumberland','22' :'Dauphin',
    '23' :'Delaware','24' :'Elk','25' :'Erie','26' :'Fayette','27' :'Forest','28' :'Franklin',
    '29' :'Fulton',
    '30' :'Greene','31' :'Huntingdon','32' :'Indiana','33' :'Jefferson','34' :'Juniata',
    '35' :'Lackawanna','36' :'Lancaster',
    '37' :'Lawrence','38' :'Lebanon','39' :'Lehigh','40' :'Luzerne','41' :'Lycoming','42' :'McKean',
    '43' :'Mercer',
    '44' :'Mifflin',
    '45' :'Monroe','46' :'Montgomery','47' :'Montour','48' :'Northampton','49' :'Northumberland',
    '50' :'Perry','51' :'Pike',
    '52' :'Potter',
    '53' :'Schuylkill','54' :'Snyder','55' :'Somerset','56' :'Sullivan','57' :'Susquehanna',
    '58' :'Tioga','59' :'Union',
    '60' :'Venango',
    '61' :'Warren','62' :'Washington','63' :'Wayne','64' :'Westmoreland','65' :'Wyoming',
    '66' :'York','67' :'Philadelphia'
    }




def extract():
    """
    Extracts data from a URL. Returns the data extracted as a dictionary.
    """
    URL = 'http://data.pa.gov/resource/v4w5-ixba.json'

    # Get JSON data from the URL
    response = urllib2.urlopen(URL)
    extracted_data  = json.load(response)

    return extracted_data

def transform(data):
    """
    Parses extracted_data into a list of dictionaries of the DataPoint form:
        county: string
        measure_1: Number
        measure_2: Number
        ...
        measure_n: Number
    """
    data_points = []
    county_data_set = []

    for datum in data:
        handicap = 0
        parking = 0
        if 'handicap_space_count' in datum.keys():
            handicap = int(datum['handicap_space_count'])
        if 'parking_space_count' in datum.keys():
            parking = int(datum['parking_space_count'])
        county_datum = {
            "handicap_space_count": handicap,
            "county": CODE_COUNTY[datum['county_code']],
            "parking_space_count": parking,
            "park_and_ride_count": 1
        }
        county_data_set.append(county_datum)

    correction_dataframe = pd.DataFrame.from_dict(county_data_set)

    agg_function_sum = {'parking_space_count': ['sum'],'handicap_space_count': ['sum'],'park_and_ride_count': ['sum']}
    correction_dataframe = correction_dataframe.groupby(["county"]).agg(agg_function_sum)

    correction_dataframe.reset_index(inplace=True)
    correction_dataframe.columns = pd.Index(['county','park_and_ride_count','handicap_space_count','parking_space_count'])

    return correction_dataframe.T.to_dict().values()

def load(records):
    """
    Construct the document for ElasticSearch
    """
    document = {
        'id': 'b55e-zfp9',
        'name': 'Park and Ride Locations Current Transportation',
        'categories': ['transportation','recreation','environment'],
        'tags': ['location','pdot','ride,park'],
        'measures': ['park_and_ride_count','handicap_space_count','parking_space_count'],
        'data': records
    }

    with open(DATA_FILE_PATH, 'w') as data_file:
        data_file.write(json.dumps(document))

    return document


data = extract()
data_points = transform(data)
document = load(data_points)
pprint(document)
