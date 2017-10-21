#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 12:49:52 2017

@author: geoffrey.kip
"""

import json
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
import psycopg2



con = psycopg2.connect( host= hostname, user= username, password= password, database=database)
cur = con.cursor()  

DATASET_FILES = [
    "data/hospitalization.json",
    "data/jobs.json",
    "data/medicaid.json",
    "data/prisons.json",
    "data/snap.json",
    "data/unemployment.json",
    "data/low_birth_weight.json",
    "data/poverty.json"    
]

def parse_json(data):
    data= pd.DataFrame(data['data'])
    data_measures= data[data.columns.difference(['county','date'])]
    data_info= data.loc[:,['county', 'date']]
    results=[]
    for i in data_measures.index:
        data=data_measures.loc[i].to_json()
        results.append(data)
    measures=pd.DataFrame(results)
    measures.columns=['measures']
    data= pd.merge(data_info, measures, how='left', left_index=True, right_index=True)
    return data

def shape_data(data):
    """
    Shapes data into format for loading into database
    """
    data= pd.DataFrame(data["data"])
    data["date"]=pd.to_datetime(data['date'])
    data['year'] = data['date'].dt.year
    data['month'] = data['date'].dt.month
    data= data.drop("date", axis=1)
    return data

def load_dataset_file(dataset_file):
    """
    Loads dataset
    """
    with open(dataset_file) as f:
        data = json.load(f)
        return data

# NOTE: Load all the files 

datasets = list(map(load_dataset_file, DATASET_FILES))
  
measures_clause=""
for i in range(len(datasets)):
    results= datasets[i]["measures"]
    for results in results:
       measures_clause += results + " numeric null,"

measures_clause= measures_clause[:-1]

cur.execute("DROP TABLE IF EXISTS data_points")
cur.execute("CREATE TABLE data_points(id SERIAL, index int,  data_set_id integer, county text,\
            year int,  month int, %s)" % measures_clause)
query =  "INSERT INTO data_points (Id, data_set_id, county,date,measures) VALUES (%s, %s, %s,%s,%s);"
con.commit()
    

#load into postgresql  
results = list(map(shape_data, datasets))
     
#load these datasets into postgresql database  
for i in range(len(results)):
    results[i].to_sql("data_points", engine, if_exists='append')       

      
