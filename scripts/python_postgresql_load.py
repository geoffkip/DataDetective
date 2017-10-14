#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 12:49:52 2017

@author: geoffrey.kip
"""

import json
import pandas as pd
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

con = psycopg2.connect( host= hostname, user= username, password= password, database=database)
cur = con.cursor()  
engine = create_engine('postgresql://postgres:titans@35.196.134.129:5432/postgres')

cur.execute("DROP TABLE IF EXISTS data_points")
cur.execute("CREATE TABLE data_points(Id SERIAL, data_set_id integer, county text,\
            date date, measures json)")
query =  "INSERT INTO data_points (Id, data_set_id, county,date,measures) VALUES (%s, %s, %s,%s,%s);"
con.commit()

def without_keys(d, keys):
      return {x: d[x] for x in d if x not in keys}

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

with open("data/jobs.json") as jobs_data:
    PA_jobs = json.load(jobs_data)
    print(PA_jobs)

with open("data/trainings.json") as trainings_data:
    PA_trainings = json.load(trainings_data)
    print(PA_trainings)

with open("data/medicaid.json") as medicaid_data:
    PA_medicaid = json.load(medicaid_data)
    print(PA_medicaid)

with open("data/prisons.json") as prisons_data:
    PA_prisons = json.load(prisons_data)
    print(PA_prisons)
    
with open("data/corrections_pop.json") as corrections_data:
    PA_corrections = json.load(corrections_data)
    print(PA_corrections)
    
with open("data/snap.json") as snap_data:
    PA_snap = json.load(snap_data)
    print(PA_snap)
    
    
#Create datasets for loading into postgressql
Jobs_datasets= without_keys(PA_jobs,{"data"})
Jobs_datasets["data_set_id"] = 1
Trainings_datasets= without_keys(PA_trainings,{"data"})
#Trainings_datasets["data_set_id"] = 2
Medicaid_datasets= without_keys(PA_medicaid,{"data", "measures"})
Medicaid_datasets["data_set_id"] = 2
Corrections_datasets= without_keys(PA_corrections,{"data", "measures"})
Corrections_datasets["data_set_id"]= 3
Snap_datasets= without_keys(PA_snap,{"data"})
Snap_datasets["data_set_id"]=4
Prisons_datasets= without_keys(PA_prisons, {"data", "measures"})
Prisons_datasets["data_set_id"]= 5

#parse json files to create data points datasets for loading into postgresql    
Jobs_data_points= parse_json(PA_jobs)
Jobs_data_points["data_set_id"] = 1
#PA_trainings= without_keys(PA_trainings,exclude)
Medicaid_data_points= parse_json(PA_medicaid)
Medicaid_data_points["data_set_id"] = 2
Prisons_data_points= parse_json(PA_prisons)
Prisons_data_points["data_set_id"] = 3
Corrections_data_points= parse_json(PA_corrections)
Corrections_data_points["data_set_id"] = 4
Snap_data_points= parse_json(PA_snap)
Snap_data_points["data_set_id"] = 5
     
#load these datasets into postgresql database   
             
Jobs_data_points.to_sql("data_points", engine, if_exists='replace')
Medicaid_data_points.to_sql("data_points", engine, if_exists='replace')
Prisons_data_points.to_sql("data_points", engine, if_exists='replace')
Corrections_data_points.to_sql("data_points", engine, if_exists='replace')
Snap_data_points.to_sql("data_points", engine, if_exists='replace')

      
 #Export as csvs
Jobs_data_points.to_csv("data/jobs_psql.csv", sep=',', encoding='utf-8',index=False)               
Medicaid_data_points.to_csv("data/medicaid_psql.csv", sep=',', encoding='utf-8',index=False)
Prisons_data_points.to_csv("data/prisons_psql.csv", sep=',', encoding='utf-8',index=False)
Corrections_data_points.to_csv("data/corrections_psql.csv", sep=',', encoding='utf-8',index=False)
Snap_data_points.to_csv("data/snap_psql.csv", sep=',', encoding='utf-8',index=False)
