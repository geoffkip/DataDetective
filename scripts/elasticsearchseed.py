"""

ElasticSearch Seed:

This script loads all the parse data into ElasticSearch idempotently.

Requires environmental variables be set:
    - ES_HOST
    - ES_USER
    - ES_PASS

"""
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch_dsl import *
from pprint import pprint
import os
import json


elasticSearchConnectionString = 'http://' + os.environ['ES_USER']+':' + os.environ['ES_PASS'] + '@' + os.environ['ES_HOST']
es = Elasticsearch(elasticSearchConnectionString)
try: # to delete the index if it exists (for idempotentcy)
    es.indices.delete(index='paindex')
except NotFoundError as e:
    pass

DATASET_FILES = [
    "data/corrections.json",
    "data/hospitalization.json",
    "data/jobs.json",
    "data/medicaid.json",
    "data/park_n_ride.json",
    "data/poverty.json",
    "data/prisons.json",
    "data/snap.json",
    "data/unemploment.json"
]

def load_dataset_file(dataset_file):
    """
    Loads a data set into ElasticSearch
    """
    with open(dataset_file) as f:
        data = json.load(f)
        document = {
            'external_id': data["id"],
            'tags':        data["tags"],
            'categories':  data["categories"],
            'measures':    data["measures"]
        }
        res = es.index(index="paindex", doc_type='PA', body=document)
        if not res['created']:
            raise Exception("File %s could not be created." % dataset_file)
        else:
            pprint("Successfully loaded %s" % dataset_file)
            pprint(document)


    return

# NOTE: Load all the files into ElasticSearch
for dataset_file in DATASET_FILES:
    load_dataset_file(dataset_file)
