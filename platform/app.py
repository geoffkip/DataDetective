# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
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

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children="Data Detective"),

    html.Div(children='''
    Total Jobs by County
    '''
    ),

    dcc.Graph(
        id='Time-series-graph',
        figure = {
        'data' : [go.Bar(
                  x= data.date[data['county'] == county],
                  y= data.total_jobs[data['county'] == county],
                  name= county) for county in data['county'].unique()],
        'layout' : go.Layout(
        barmode='stack',
        xaxis = {
            'title' : 'Date',
        },
        yaxis = {
            'title' : 'Total Jobs'
        })
    }
)])

if __name__ == '__main__':
    app.run_server(debug=True)
