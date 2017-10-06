# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from elasticsearch import Elasticsearch
from elasticsearch_dsl import *
import plotly.graph_objs as go
import pandas as pd

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
res = es.search(index="paindex", body={"query": {"match_all": {}}})
data=pd.DataFrame(res["hits"]["hits"][0]["_source"]["data"])
data["date"]=pd.to_datetime(data['date'])
data= data.groupby(["county", "date"]).sum()
data.reset_index(inplace=True)
data=data.sort_values('date')

counties= data['county'].unique()

app = dash.Dash()

app.layout = html.Div([

    html.H1("Data Detective"),

    html.Div([
    html.Label('County'),
    dcc.Dropdown(
        id='county',
        options=[{'label': i, 'value': i} for i in counties],
        value=['Philadelphia']
    ),

    html.Label('Measure'),
    dcc.Dropdown(
        id='Measure',
        options=[
            { 'label': 'Jobs', 'value': 'Jobs'},
            {'label': 'Schools', 'value': 'Schools'}
        ],
        value=['Jobs', 'Schools'],
        multi=True
    )]),

    dcc.Graph(
        id='time-series-graph')
])

@app.callback(
    dash.dependencies.Output('time-series-graph', 'figure'),
    [dash.dependencies.Input('county', 'value')])
def update_graph(selected_county):
    return {
        'data' : [go.Scatter(
                  x= data.date[data['county'] == selected_county],
                  y= data.total_jobs[data['county'] == selected_county],
                  name= selected_county)],
        'layout' : go.Layout(
        xaxis = {
            'title' : 'Date',
        },
        yaxis = {
            'title' : 'Total Jobs'
        })
        }



if __name__ == '__main__':
    app.run_server(debug=True)
