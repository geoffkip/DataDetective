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
    data_id = None
    definition = None
    metadata = None

    def __init__(self, definition=None, definition_path=None, metadata=None):
        if self.definition == None:
            if definition != None:
                self.definition = definition
            elif definition_path != None:
                with open(definition_path) as data_file:
                    self.definition = json.load(data_file)

    def extract(self, url=None):
        """
        Extracts data from a URL. Returns the data extracted as a list of dictionaries.
        Also extracts the metadata for the data set and stores it
        """
        if self.definition['data_id'] != None:
            self.data_id = self.definition['data_id']

        data_url = "http://data.pa.gov/resource/%s.json" % self.definition['data_id']
        metadata_url = "http://data.pa.gov/api/views/%s.json" % self.definition['data_id']

        data_response = urllib2.urlopen(data_url)
        extracted_data = json.load(data_response)

        metadata_response = urllib2.urlopen(metadata_url)
        metadata = json.load(metadata_response)

        return {"data": extracted_data, "metadata": metadata}

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
                if path_item in value.keys():
                    value = value[path_item]
        else:
            value = path
        return value


    def load(self, records, metadata):
        """
        Construct the document for ElasticSearch
        """
        document = {
            'id': metadata['id'],
            'name': metadata['name'],
            'category': metadata['category'],
            'tags': metadata['tags'],
            'description': metadata['description'],
            'attribution': metadata['attribution'],
            'data': records
        }

        # TODO: Write to ElasticSearch
        # with open(DATA_FILE_PATH, 'w') as data_file:
        #     data_file.write(json.dumps(document))

        return document


    def etl(self):
        data = self.extract()
        data_points = self.transform(data)
        documents = self.load(data_points)
