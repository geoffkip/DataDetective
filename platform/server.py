from flask import Flask, render_template, request, session, redirect, url_for
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
from flask import jsonify
import pandas as pd

app = Flask(__name__)

#Initialize elasticsearch with flask app
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
res = es.search(index="paindex", body={"query": {"match_all": {}}})

COUNTIES_LIST= All_data['county'].unique()
MEASURES_LIST= All_data[All_data.columns.difference(['county','date'])]

@app.route('/')
def index():
    return 'Data Detective App'

#Test to see if data prints out
@app.route('/elasticsearch')
def elasticsearch():
    return jsonify(res),200

@app.route('/counties/list')
def counties():
    return jsonify(counties_list),200

@app.route('/measures/list')
def measures():
    return jsonify(measures_list),200


if __name__ == '__main__':
    app.run(debug=True)
