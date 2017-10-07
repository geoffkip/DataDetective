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
jobs_data=pd.DataFrame(res["hits"]["hits"][0]["_source"]["data"])
jobs_data["date"]=pd.to_datetime(jobs_data['date'])
jobs_data= jobs_data.groupby(["county", "date"]).sum()
jobs_data.reset_index(inplace=True)
jobs_data=jobs_data.sort_values('date')

trainings_data=pd.DataFrame(res["hits"]["hits"][1]["_source"]["data"])
# trainings_data["date"]=pd.to_datetime(trainings_data['date'])
# trainings_data= trainings_data.groupby(["county", "date"]).sum()
# trainings_data.reset_index(inplace=True)
# trainings_data=trainings_data.sort_values('date')

medicaid_data=pd.DataFrame(res["hits"]["hits"][2]["_source"]["data"])
medicaid_data["date"]=pd.to_datetime(medicaid_data['date'])
medicaid_data.rename(columns={'county_name': 'county'}, inplace=True)
medicaid_data= medicaid_data.groupby(["county", "date"]).sum()
medicaid_data.reset_index(inplace=True)
medicaid_data=medicaid_data.sort_values('date')

prison_data=pd.DataFrame(res["hits"]["hits"][3]["_source"]["data"])
prison_data["date"]=pd.to_datetime(prison_data['date'])
prison_data= prison_data.groupby(["county", "date"]).sum()
prison_data.reset_index(inplace=True)
prison_data=prison_data.sort_values('date')

All_data=pd.concat([jobs_data,trainings_data,medicaid_data,prison_data])
All_data= All_data.sort_values('date')

counties= All_data['county'].unique()
measures= All_data[All_data.columns.difference(['county','date'])]

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

    html.Label('Measures'),
    dcc.Dropdown(
        id='measures',
        options=[{'label': i, 'value': i} for i in measures],
        value=['total_jobs']
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
                  x= All_data.date[All_data['county'] == selected_county],
                  y= All_data.total_jobs[All_data['county'] == selected_county],
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
