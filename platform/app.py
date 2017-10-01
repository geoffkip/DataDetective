from flask import Flask, render_template, request, session, redirect, url_for
from flask.ext.elasticsearch import FlaskElasticsearch
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
from flask import jsonify

app = Flask(__name__)

#Initialize elasticsearch with flask app
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/')
def index():
    return 'Data Detective App'

#Test to see if data prints out
@app.route('/elasticsearch')
def elasticsearch():
    s = Search(using=es)
    res = es.search(index="paindex", body={"query": {"match_all": {}}})
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
