from flask import Flask, render_template, request, session, redirect, url_for
from flask.ext.elasticsearch import FlaskElasticsearch
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
from flask import jsonify
import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='gjerome1991', api_key='JTNvEeVmv04ADNFHYTIJ')


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


@app.route('/datadetective')
def plot():
    res = es.search(index="paindex", body={"query": {"match_all": {}}})
    data=pd.DataFrame(res["hits"]["hits"][0]["_source"]["data"])
    data["date"]=pd.to_datetime(data['date'])
    data= data.groupby(["county", "date"]).sum()
    data.reset_index(inplace=True)
    data=data.sort_values('date')

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

    plot= py.image.ishow(fig)



if __name__ == '__main__':
    app.run(debug=True)
