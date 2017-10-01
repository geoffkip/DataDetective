from datetime import datetime
from pprint import pprint
import urllib2
import json

"""
Sample:
{
    "countyname":"Luzerne",
    "jobs_pledged_to_be_created":"0",
    "jobs_pledged_to_be_retained":"33",
    "month":"July",
    "total_jobs":"33",
    "year":"2016"
}
"""

DATA_FILE_PATH = 'data/jobs.json'

def extract():
    """
    Extracts data from a URL. Returns the data extracted as a dictionary.
    """
    URL = 'http://data.pa.gov/resource/sshd-za9g.json'

    # Get JSON data from the URL
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
        #print (resource.keys())
        county                      = datum["countyname"]
        date                        = datetime.strptime('%s %s'%(datum["month"],datum["year"]),'%B %Y')
        jobs_pledged_to_be_created  = int(datum["jobs_pledged_to_be_created"])
        jobs_pledged_to_be_retained = int(datum["jobs_pledged_to_be_retained"])
        total_jobs                  = int(datum["total_jobs"])

        data_point = {
            'county': county,
            'date': date.strftime('%Y-%m-%d'),
            'jobs_pledged_to_be_created': jobs_pledged_to_be_created,
            'jobs_pledged_to_be_retained': jobs_pledged_to_be_retained,
            'total_jobs': total_jobs
        }

        data_points.append(data_point)

    return data_points

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

data = extract()
data_points = transform(data)
document = load(data_points)
pprint(document)
