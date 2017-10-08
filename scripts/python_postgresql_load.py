#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 12:49:52 2017

@author: geoffrey.kip
"""

import json

def without_keys(d, keys):
      return {x: d[x] for x in d if x not in keys}

def parse_json(data):
    for i in range(len(data["data"])):
        data[i]= {"id": data["id"],
           "county": data["data"][i]["county"],
           "date": data["data"][i]["date"],
           "json": without_keys(data["data"][i],invalid)}

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
    
invalid= {"county","date"}      
exclude= {"categories","data", "tags", "name", "id", "measures"}

#Create datasets for loading into postgressql
Jobs_datasets= without_keys(PA_jobs,{"data"})
Trainings_datasets= without_keys(PA_trainings,{"data"})
Medicaid_datasets= without_keys(PA_medicaid,{"data", "measures"})
Corrections_datasets= without_keys(PA_corrections,{"data", "measures"})
Snap_datasets= without_keys(PA_snap,{"data"})
Prisons_datasets= without_keys(PA_prisons, {"data", "measures"})

#parse json files to create data points datasets for loading into postgresql
parse_json(PA_jobs)
#parse_json(PA_trainings)
parse_json(PA_medicaid)
parse_json(PA_prisons)
parse_json(PA_corrections)
parse_json(PA_snap)
    
Jobs_data_points= without_keys(PA_jobs,exclude)
#PA_trainings= without_keys(PA_trainings,exclude)
Medicaid_data_points= without_keys(PA_medicaid,exclude)
Prisons_data_points= without_keys(PA_prisons,exclude)
Corrections_data_points= without_keys(PA_corrections,exclude)
Snap_data_points= without_keys(PA_snap,exclude)