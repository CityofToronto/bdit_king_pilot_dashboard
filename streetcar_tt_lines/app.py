import json
import itertools
import os

import plotly.graph_objs as go

import pandas
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
# In case there are problems with react loading from unpkg, set to True
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False

app.layout = html.Div(children=[html.Div(html.H2('Click on a segment to view average travel times for it.')),
                                html.Div(children=[html.Div(dcc.Graph(id='travel-time-graph'))])
                               ])

streetcar_df = pandas.read_csv('../data/streetcar_travel_times.csv')

# @app.callback(
#     Output('travel-time-graph', 'figure'),
#     [])
def update_graph(segment):
    
    title = 'Graph Title'
    
    
    data = [go.Scatter(x=streetcar_df['Month'],
                   y=streetcar_df['Travel Time'],
                   mode='lines')]
    layout = dict(title = 'Average Weekday Travel Times <br>' +title,
                  xaxis = dict(title="Month"),
                  yaxis = dict(title="Travel Time (min)"))
    
    return {'data':data, 'layout':layout}

if __name__ == '__main__':
    app.run_server(debug=True)
