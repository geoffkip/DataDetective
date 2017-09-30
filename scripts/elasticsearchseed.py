#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 15:42:15 2017

@author: geoffrey.kip
"""
from datetime import datetime
import requests
from elasticsearch import Elasticsearch

# make sure ES is up and running
res = requests.get('http://localhost:9200')
print(res.content)
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

doc1 = {
    'id': 'dv4n-h3dn',
    'name': 'School Performance' ,
    'categories': ["Education", "Health"] ,
    'tags': ["Bridges"],
    'data': [{"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            },

            {"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            },
             
             {"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            }] ,
}
    
doc2 = {
    'id': 'dv4n-h3dn',
    'name': 'School Performance' ,
    'categories': ["Education", "Health"] ,
    'tags': ["Bridges"],
    'data': [{"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            },

            {"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            },
             
             {"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            }] ,
}
    
doc3 = {
    'id': 'dv4n-h3dn',
    'name': 'School Performance' ,
    'categories': ["Education", "Health"] ,
    'tags': ["Bridges"],
    'data': [{"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            },

            {"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            },
             
             {"date":"2017-09-27",
              "county": "Bucks",
              "dollars" : 20 ,
              "applicants": 2
            }] ,
}
    
    
    
#index some test data
res= es.index(index="paindex", doc_type='PA', body=doc)
print(res['created'])

res = es.get(index="paindex", doc_type='PA', id=1)
print(res['_source'])

es.indices.refresh(index="paindex")

res = es.search(index="paindex", body={"query": {"match_all": {}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(applicants)s %(county)s: %(dollars)s" % hit["_source"])