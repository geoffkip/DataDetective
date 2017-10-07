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

class Translator(object):
    data_url = None
    definition = None

    def __init__(self, definition=None, definition_path=None):
        if self.definition == None:
            if definition != None:
                self.definition = definition
            elif definition_path != None:
                with open(definition_path) as data_file:
                    self.definition = json.load(data_file)

    def extract(self, url=None):
        """
        Extracts data from a URL. Returns the data extracted as a list of dictionaries.
        """
        if url is not None:
            self.data_url = url
        elif self.definition['data_id'] != None:
            self.data_url = "http://data.pa.gov/resource/%s.json" % self.definition['data_id']

        response = urllib2.urlopen(self.data_url)
        extracted_data = json.load(response)

        return extracted_data

    def transform(self, data):
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
            data_point = dict()
            for key, value in self.definition['data_point'].items():
                if isinstance(value, (list, tuple)):
                    points = list()
                    for item in value:
                        points.append(self.getDataPoint(item, datum))
                    data_point[key] = self.transformDataValue(key, points)
                else:
                    data_point[key] = self.transformDataValue(key, self.getDataPoint(value, datum))

            data_points.append(data_point)

        return data_points

    def transformDataValue(self, column, value):
        return value

    def getDataPoint(self, path, datum):
        value = None
        if "data_point." in path:
            path = path.split('.')
            del path[0]
            value = datum
            for path_item in path:
                value = value[path_item]
        else:
            value = path
        return value


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


    def etl(self):
        data = self.extract()
        data_points = self.transform(data)
        documents = self.load(data_points)
