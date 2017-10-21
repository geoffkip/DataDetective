import sys, os, os.path, binascii
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),"lib"))
from flask import Flask, render_template, request, session, redirect, url_for
from flask import jsonify
from collections import Counter
import config
import recommender
import database
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', page="home")

@app.route('/tools/maps')
def tools_maps():
    return render_template('tools/maps.html', page="maps")

@app.route('/tools/lines')
def tools_lines():
    return render_template('tools/lines.html', page="lines")

@app.route('/tools/columns')
def tools_columns():
    return render_template('tools/columns.html', page="columns")

@app.route('/measures/<measure>', methods=['POST'])
def measure_data(measure):
    """
    Returns the data for a given measure, year, and month as JSON that
    can be used as a series in a HighChart:

    {
      "data": [
        ['County 1', 100],
        ['County 2', 100],
        ...
        ['County n', 100]
      ],
      "name": 'Measure Name'
    }
    """
    year =  request.form['year']
    month = request.form['month']

    data = database.get_measure_data(measure, year, month)

    return jsonify(data),200

@app.route('/measures/<measure>/timeseries', methods=['POST'])
def measure_data_timeseries(measure):
    """
    Returns the data for a given measure for timeseries HighChart
    """

    return jsonify(config.generate_timeseries(measure)),200


@app.route('/measures/recommend', methods=['POST'])
def recommend():
    """
    Returns a list of measure similar to the list of measures.
    """
    selected_measures =  request.form["measures"].replace('"','').split(',')
    tags, categories = recommender.get_tags_categories(selected_measures)
    recommended_measures = recommender.get_measures(tags, categories)
    unduplicated_measures=list(set(recommended_measures) - set(selected_measures))
    return jsonify(unduplicated_measures),200

@app.route('/counties/list')
def counties():
    """
    Returns a list of all counties in PA.
    """
    return jsonify(config.COUNTIES),200

@app.route('/measures/list')
def measures():
    """
    Returns the list of all measures stored in the database.
    """
    measures = recommender.get_measures([],[])
    return jsonify(measures),200

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
