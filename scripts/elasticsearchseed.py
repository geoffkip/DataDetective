#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 15:42:15 2017

@author: geoffrey.kip
"""
from datetime import datetime
import requests
from elasticsearch import Elasticsearch 
from elasticsearch_dsl import *
import json

# make sure ES is up and running
res = requests.get('http://localhost:9200')
print(res.content)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
s = Search(using=es)

#load real data

es.indices.delete(index='paindex')

with open("/Users/geoffrey.kip/DataDetective/data/jobs.json") as json_data:
    PA_data = json.load(json_data)
    print(PA_data)
    
res= es.index(index="paindex", doc_type='PA', body=PA_data)
print(res['created'])

es.indices.refresh(index="paindex")

res = es.search(index="paindex", body={"query": {"match_all": {}}})
print(res)

# Search queries
# searching for id

s = s.query("multi_match", query='d5pf-ti7w', fields=['id'])
response = s.execute()

res = es.search(index="paindex", body={"query": {"match_all": {}}})
print("%d documents found" % res['hits']['total'])


