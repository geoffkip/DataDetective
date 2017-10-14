"""
Wrapper for ElasticSearch
"""
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *

def connection():
    """
    Establishes a connection to the ElasticSearch server
    """
    return Elasticsearch('http://elastic:changeme@localhost:9200')

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

    # TODO: Parse measures from res

    return measures
