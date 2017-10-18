"""
Wrapper for ElasticSearch

Requires environmental variables be set:
    - ES_HOST
    - ES_USER
    - ES_PASS
"""
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
import os

def connection():
    """
    Establishes a connection to the ElasticSearch server
    """
    elasticSearchConnectionString = 'http://' + os.environ['ES_USER']+':' + os.environ['ES_PASS'] + '@' + os.environ['ES_HOST']
    return Elasticsearch(elasticSearchConnectionString)

def get_tags_categories(measures):
    """
    Returns a list of tags and categories for these
    """
    mustList = []
    for measure in measures:
        mustList.append({"match": {"measures": {"value" : measure}}})
    res = connection().search(index="paindex", body={"query":{"bool": {"must": mustList }}})
    tags, categories = parse_tags_categories(res)
    return tags, categories

def parse_tags_categories(response):
    """
    Returns a list of tags and categories for json response from elasticsearch
    """
    responsedatasets = response['hits']['hits']
    tags = []
    categories = []
    for responsedataset in responsedatasets:
        _tags = responsedataset['_source']['tags']
        _categories = responsedataset['_source']['categories']
        for tag in _tags:
            tags.append(tag)
        for category in _categories:
            categories.append(category)
    return tags, categories

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
