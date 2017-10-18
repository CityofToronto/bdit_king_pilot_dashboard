# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:39:25 2017

@author: rrodger
"""


import pandas
from datetime import date, datetime
import dash
import dash_core_components as core
import dash_html_components as html
import plotly.graph_objs as go


times = pandas.read_csv('car_travel_times.csv')

middate = date(2017, 10, 2)

streets = ['Dundas', 'Queen']

def getFig(street, midDate, times): #returns a graph_objs figure from a dataset.
#can be stacked/grouped if data is appropriately formatted.
    before = times.loc[(times['corridor'] == street) & (datetime.strptime(times['mon'], '%Y-%m-%d %H:%M:%S').date() <= middate)]
    after = times.loc[(times['corridor'] == street) & (datetime.strptime(times['mon'], '%Y-%m-%d %H:%M:%S').date() >= middate)]
    
    fig1 = go.Bar(x = before['dir'],
                  y = before['travel_time'],
                  name = 'Before')
    
    fig2 = go.Bar(x = after['dir'],
                  y = after['travel_time'],
                  name = 'After')
    
    layout = go.Layout(barmode = 'group',
                       title = street,
                       xaxis = dict(title = 'Before/After'),
                       yaxis = dict(title = 'Travel Time'))
    
    data = [fig1, fig2]
    
    return go.Figure(data = data, layout = layout)
    


app = dash.Dash()
server = app.server


#Generates a list of graphs in divs for each street in a list.

graphdivs = [html.Div(core.Graph(id = ('traveltime_' + street), figure = getFig(street, middate, times))) for street in streets] #, core.Graph(id = ('traveltime_' + streets[1]), figure = figures[1])]
app.layout = html.Div([core.RadioItems(
                id = 'streetname',
                options=[{'label' : timebucket, 'value' : timebucket} for timebucket in ('AM','PM')],
                value = 'AM'),
                html.Div(graphdivs)])
#interactivity
#==============================================================================
# @app.callback(
#     [dash.dependencies.Output(['traveltime_' + street, 'figure' for street in streets])]
#     dash.dependencies.input('Manager', 'value'))
#
#def update_graph()
#==============================================================================

if __name__ == '__main__':
    app.run_server(debug=True)
