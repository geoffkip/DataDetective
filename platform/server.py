import sys, os, os.path, binascii
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),"lib"))
from flask import Flask, render_template, request, session, redirect, url_for
from flask import jsonify
import config
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
      "name": 'Measure Name (date_1)'
    }
    """
    year =  request.form['year']
    month = request.form['month']

    # TODO: Fetch the data for this measure from the database.
    # data = get_measure_data(measure, year, month)

    return jsonify(config.SERIES),200

@app.route('/measures/recommend', methods=['POST'])
def recommend():
    """
    Returns a list of measure similar to the list of measures.
    """
    measures =  request.get_json()["measures"]
    tags, categories = recommender.get_tags_categories(measures)
    measures = recommender.get_measures(tags, categories)
    return jsonify(measures),200


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

    # TODO: Get this returning a list of all measures
    #       Probably best to initialize the list of measures
    #       once when the application is first initialized.

    return jsonify(config.MEASURES),200


if __name__ == '__main__':
    app.run(debug=True)
