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

times['mon'] = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S').date() for i in times['mon']]

middate = date(2017, 10, 2)

streets = ['Dundas', 'Queen', 'Adelaide', 'Front', 'Richmond', 'Wellington']

def getfig(street, AMPM): #returns a graph_objs figure from a dataset.
#can be stacked/grouped if data is appropriately formatted.
    befAP = before[street].loc[(before[street]['time_period'] == AMPM)]
    aftAP = after[street].loc[(after[street]['time_period'] == AMPM)]
    

    
    fig1 = go.Bar(x = befAP['dir'],
                  y = befAP['travel_time'],
                  name = 'Before')
    
    fig2 = go.Bar(x = aftAP['dir'],
                  y = aftAP['travel_time'],
                  name = 'After')
    
    layout = go.Layout(barmode = 'group',
                       title = street,
                       xaxis = dict(title = 'Before/After'),
                       yaxis = dict(title = 'Travel Time'))
    
    return {'data' : [fig1, fig2],
            'layout' : layout}
    


app = dash.Dash()
server = app.server


#Generates a list of graphs in divs for each street in a list.

#graphdivs = [html.Div(core.Graph(id = ('traveltime_' + street), figure = getFig(street, middate, times))) for street in streets] #, core.Graph(id = ('traveltime_' + streets[1]), figure = figures[1])]

before = {street : times.loc[(times['corridor'] == street) & (times['mon'] <= middate)] for street in streets}
after = {street : times.loc[(times['corridor'] == street) & (times['mon'] >= middate)] for street in streets}


app.layout = html.Div([core.RadioItems(
                id = 'AMPM',
                options=[{'label' : timebucket, 'value' : timebucket} for timebucket in times['time_period'].unique()],
                value = 'AM'),
                
                core.Graph(id = streets[0]),
                core.Graph(id = streets[1]),
                core.Graph(id = streets[2]),
                core.Graph(id = streets[3]),
                core.Graph(id = streets[4]),
                core.Graph(id = streets[5])])
#interactivity
@app.callback(
#    [dash.dependencies.Output('traveltime_' + street, 'figure')for street in streets]
    dash.dependencies.Output(streets[0], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_dundas(AMPM):
    #return [html.Div(core.Graph(id = ('traveltime_' + street), figure = getFig(street, middate, times))) for street in streets] #, core.Graph(id = ('traveltime_' + streets[1]), figure = figures[1])]
#==============================================================================
#     b1 = before.loc[before['time_period'] == AMPM]
#     a1 = after.loc[after['time_period'] == AMPM]
#   
#     fig1 = go.Bar(x = b1['dir'],
#                   y = b1['travel_time'],
#                   name = 'Before')
#     
#     fig2 = go.Bar(x = a1['dir'],
#                   y = a1['travel_time'],
#                   name = 'After')
# 
#     layout = go.Layout(barmode = 'group',
#                        title = streets[0],
#                        xaxis = dict(title = 'Before/After'),
#                        yaxis = dict(title = 'Travel Time'))
#==============================================================================
    
    
    return getfig(streets[0], AMPM)

@app.callback(
#    [dash.dependencies.Output('traveltime_' + street, 'figure')for street in streets]
    dash.dependencies.Output(streets[1], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_queen(AMPM):
    return getfig(streets[1], AMPM)

@app.callback(
#    [dash.dependencies.Output('traveltime_' + street, 'figure')for street in streets]
    dash.dependencies.Output(streets[2], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_adelaide(AMPM):
    return getfig(streets[2], AMPM)

@app.callback(
#    [dash.dependencies.Output('traveltime_' + street, 'figure')for street in streets]
    dash.dependencies.Output(streets[3], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_front(AMPM):
    return getfig(streets[3], AMPM)

@app.callback(
#    [dash.dependencies.Output('traveltime_' + street, 'figure')for street in streets]
    dash.dependencies.Output(streets[4], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_richmond(AMPM):
    return getfig(streets[4], AMPM)

@app.callback(
#    [dash.dependencies.Output('traveltime_' + street, 'figure')for street in streets]
    dash.dependencies.Output(streets[5], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_wellington(AMPM):
    return getfig(streets[5], AMPM)



if __name__ == '__main__':
    app.run_server(debug=True)

