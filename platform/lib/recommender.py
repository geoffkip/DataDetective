"""
Wrapper for ElasticSearch
"""
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *

def connection():
    """
    Establishes a connection to the ElasticSearch server
    """
    return Elasticsearch('http://elastic:changeme@35.190.137.232:9200')

def get_measures(tags, categories):
    """
    Returns a list of measures relevant to these tags and categories
    """
    shouldList = []
    for tag in tags:
        shouldList.append({"fuzzy": {"tags": {"value" : tag}}})
    for category in categories:
        shouldList.append({"fuzzy": {"tags": {"value" : category}}})
    res = connection().search(index="paindex", body={"query":{"bool": {"should": shouldList }}})
    measures = parse_measures(res)
    return measures
def parse_measures(response):
    """
    Returns a list of measures for json response from elasticsearch
    """
    responsedatasets = response['hits']['hits']
    measures = []
    for responsedataset in responsedatasets:
        datasetmeasures = responsedataset['_source']['measures']
        for datasetmeasure in datasetmeasures:
            measures.append(datasetmeasure)
    return measures
