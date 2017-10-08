from flask import Flask, render_template, request, session, redirect, url_for
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
from flask import jsonify
import pandas as pd

app = Flask(__name__)

COUNTIES_LIST =[{"name": "Adams"},{"name": "Armstrong"},{"name": "Beaver"},
{"name": "Bedford"},{"name": "Statewide"},{"name": "Alleghany"},
{"name": "Northampton"},{"name": "Luzerne"},{"name": "Lancaster"},
{"name": "Philadelphia"},{"name": "Washington"},{"name": "Bradford"},
{"name": "Dauphin"},{"name": "Snyder"},{"name": "Deleware"},
{"name": "Bucks"},{"name": "Montgomery"},{"name": "Lackawanna"},
{"name": "Schuylkill"}, {"name": "Mifflin"},{"name": "Franklin"},
{"name": "Union"},{"name": "York"},{"name": "Lycoming"},
{"name": "Centre"},{"name": "Blair"},{"name": "Fayette"},
{"name": "Mercer"},{"name": "Pike"},{"name": "Chester"},
{"name": "Monroe"},{"name": "Carbon"},{"name": "Indiana"},
{"name": "Huntingdon"},{"name": "Greene"},{"name": "Forest"},
{"name": "Wayne"},{"name": "Clearfield"},{"name": "Somerset"},
{"name": "Crawford"},{"name": "Norhumberland"},{"name": "Berks"},
{"name": "Tioga"},{"name": "Columbia"},{"name": "Butler"},{"name": "Susquehanna"},
{"name": "Cameron"},{"name": "Warren"},{"name": "Venango"},
{"name": "Lebanon"},{"name": "Lawrence"},{"name": "Cambria"},
{"name": "Montour"},{"name": "Juniata"},{"name": "Jefferson"},
{"name": "Clinton"},{"name": "McKean"},{"name": "Statewide Project"},
{"name": "Potter"}]

MEASURES_LIST= [{"name": "corrections_population"}, {"name": "jobs_pledged_to_be_created"},
{"name": "jobs_pledged_to_be_retained"},{"name": "corrections_population"},
{"name": "ma_individuals"},{"name": "ma_children"}, {"name": "total_jobs"}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/counties/list')
def counties():
    return jsonify(COUNTIES_LIST),200

@app.route('/measures/list')
def measures():
    return jsonify(MEASURES_LIST),200

@app.route('/chart/line')
def chart():
    return jsonify(MEASURES_LIST),200


if __name__ == '__main__':
    app.run(debug=True)
