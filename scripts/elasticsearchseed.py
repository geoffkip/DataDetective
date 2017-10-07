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
import plotly 
import plotly.plotly as py
import plotly.graph_objs as go
from functools import reduce
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

with open("/Users/geoffrey.kip/DataDetective/data/jobs.json") as jobs_data:
    PA_jobs = json.load(jobs_data)
    print(PA_jobs)
    
with open("/Users/geoffrey.kip/DataDetective/data/trainings.json") as trainings_data:
    PA_trainings = json.load(trainings_data)
    print(PA_trainings)

with open("/Users/geoffrey.kip/DataDetective/data/medicaid.json") as medicaid_data:
    PA_medicaid = json.load(medicaid_data)
    print(PA_medicaid)

with open("/Users/geoffrey.kip/DataDetective/data/prisons.json") as prisons_data:
    PA_prisons = json.load(prisons_data)
    print(PA_prisons)
    
res= es.index(index="paindex", doc_type='PA', body=PA_jobs)
print(res['created'])

res= es.index(index="paindex", doc_type='PA', body=PA_trainings)
print(res['created'])

res= es.index(index="paindex", doc_type='PA', body=PA_medicaid)
print(res['created'])

res= es.index(index="paindex", doc_type='PA', body=PA_prisons)
print(res['created'])

es.indices.refresh(index="paindex")

# Search queries
# searching for id

s = s.query("multi_match", query='d5pf-ti7w', fields=['id'])
response = s.execute()

res = es.search(index="paindex", body={"query": {"match_all": {}}})
print("%d documents found" % res['hits']['total'])
print(res)

#example how to access measures from loaded data in elasticsearch database
data=res["hits"]["hits"][0]["_source"]["data"][0]["total_jobs"]
#this grabs data from the elastic search query and formats it as a dataframe so its easier to plot
jobs_data=pd.DataFrame(res["hits"]["hits"][0]["_source"]["data"])
jobs_data["date"]=pd.to_datetime(jobs_data['date'])
jobs_data= jobs_data.groupby(["county", "date"]).sum()
jobs_data.reset_index(inplace=True)
jobs_data=jobs_data.sort_values('date')
columntypes(jobs_data)

trainings_data=pd.DataFrame(res["hits"]["hits"][1]["_source"]["data"])
trainings_data["date"]=pd.to_datetime(trainings_data['date'])
trainings_data= trainings_data.groupby(["county", "date"]).sum()
trainings_data.reset_index(inplace=True)
trainings_data=trainings_data.sort_values('date')
columntypes(trainings_data)

medicaid_data=pd.DataFrame(res["hits"]["hits"][2]["_source"]["data"])
medicaid_data["date"]=pd.to_datetime(medicaid_data['date'])
medicaid_data.rename(columns={'county_name': 'county'}, inplace=True)
medicaid_data= medicaid_data.groupby(["county", "date"]).sum()
medicaid_data.reset_index(inplace=True)
medicaid_data=medicaid_data.sort_values('date')
columntypes(medicaid_data)

prison_data=pd.DataFrame(res["hits"]["hits"][3]["_source"]["data"])
prison_data["date"]=pd.to_datetime(prison_data['date'])
prison_data= prison_data.groupby(["county", "date"]).sum()
prison_data.reset_index(inplace=True)
prison_data=prison_data.sort_values('date')
columntypes(prison_data)

All_data=pd.concat([jobs_data,trainings_data,medicaid_data,prison_data])
All_data= All_data.sort_values('date')

#==============================================================================
# dataframes=[jobs_data,prison_data, trainings_data]
# All_data = reduce(lambda  left,right: pd.merge(left,right,on=['county'],
#                                             how='outer'), dataframes)
#==============================================================================
  
traces = []
for county in data['county'].unique():
    traces.append({
        'x' : data.date[data['county'] == county],
        'y' : data.total_jobs[data['county'] == county],
        'name' : county
    })
    
fig = {
    'data' : traces,
    'layout' : {
        'title' : 'Total Jobs by County',
        'xaxis' : {
            'title' : 'Date',
        },
        'yaxis' : {
            'title' : 'Total Jobs'
        }
    }
}

py.image.ishow(fig) 
py.iplot(fig)




