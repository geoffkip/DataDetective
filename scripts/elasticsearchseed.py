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
import pandas as pd
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='gjerome1991', api_key='JTNvEeVmv04ADNFHYTIJ')

def columntypes(dataset):
    for col in dataset:
        print (col,dataset[col].dtypes)

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

#example how to access measures from loaded data in elasticsearch database
data=res["hits"]["hits"][0]["_source"]["data"][0]["total_jobs"]
#this grabs data from the elastic search query and formats it as a dataframe so its easier to plot
data=pd.DataFrame(res["hits"]["hits"][0]["_source"]["data"])
data["date"]=pd.to_datetime(data['date'])
data= data.groupby(["county", "date"]).sum()
data.reset_index(inplace=True)
data=data.sort_values('date')
columntypes(data)
data1= data[data["county"]== "Northampton"]



plot = [go.Scatter(
          x=data1.date,
          y=data1['total_jobs'])]

py.iplot(plot)




