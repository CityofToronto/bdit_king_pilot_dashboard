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
#from plotly.grid_objs import Grid, Column


times = pandas.read_csv('C:\\Users\\rrodger\\Documents\\GitHub\\bdit_king_pilot_dashboard\\car_travel_times.csv')

times['mon'] = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S').date() for i in times['mon']]

middate = date(2017, 10, 2)
streets = ['Dundas', 'Queen', 'Adelaide', 'Front', 'Richmond', 'Wellington']
h = 500
w = 1000 #graph width and height
sizemg = go.Margin(l = 20, #graph margins
              r = 20,
              b = 50,
              t = 50)
yrng = [0, times['travel_time'].max()] #All graphs have the same y axis

def getfig(street, AMPM): #returns a graph_objs figure from a dataset.
#can be stacked/grouped if data is appropriately formatted.

#Attempt at animating AM\PM transition. Make a grind with AM and PM graphs. When one is selected transition from other.
#==============================================================================
#     befPA = before[street].loc[(before[street]['time_period'] != AMPM)] #previous graph state, for animation
#     aftPA = after[street].loc[(after[street]['time_period'] != AMPM)]
#     
#     grid = Grid[befAP, aftAP, befPA, aftPA]
#==============================================================================
    
#original approach by defining figures in the function
#==============================================================================
#     fig1 = go.Bar(x = data['b' + AMPM][street]['dir'],
#                   y = data['b' + AMPM][street]['travel_time'],
#                   name = 'Before',
#                   marker = dict(color = 'rgb(0,58,114)', #bar color. Also accepts list of colors corresponding to each column
#                                  line = dict(
#                                          color = 'rgb(0,29,57)', #line color
#                                          width = 2))
#                   width = 1.5,# Also accepts list corresponding to each bar
#                   opacity = 0.5,
#                   text = "This will appear on hover and can also be a list for each column")
#==============================================================================

    
    layout = go.Layout(barmode = 'group',
                       title = street,
                       xaxis = dict(title = 'Before/After',
#                                    ,tickangle = 30,
#                                   tickfont = dict(size = 14
#                                                   color = 'rgb(204, 204, 204)'),
#                                    titlefont=dict(
#                                                   size=16,
#                                                    color='rgb(107, 107, 107)')
                                    ),
                       yaxis = dict(title = 'Travel Time',
                                    range = yrng),
#                        legend=dict(
#                                x=0,
#                                y=1.0,
#                                bgcolor='rgba(255, 255, 255, 0)',
#                                bordercolor='rgba(255, 255, 255, 0)'
#    ),
                       autosize = True,
                       annotations = ([dict(
                                       x = 'EB',
                                       y = yrng[1],
                                       text = 'this is an EB test',
                                       xanchor = 'centre',
                                       yanchor = 'top',
                                       showarrow = False),
                                        dict(
                                        x = 'WB',
                                        y = yrng[1],
                                        text = 'this is a WB test',
                                        xanchor = 'centre',
                                        yref = 'top',
                                        showarrow = False)])
               #        width = w,
               #        height = h,
               #        margin = sizemg,
                      # hovermode = False
                 #      bargap=-1,
                 #      bargroupgap=-2
                       )
    
    #frames = go.Frames
    
    return {'data' : [before_figs[AMPM][street], after_figs[AMPM][street]],
            'layout' : layout}
    


app = dash.Dash()
server = app.server

#Issue with group by. Line runs fine with dummy street and APM value. 
#print ({APM : {street : street + APM for street in streets} for APM in ('AM', 'PM')})
before_figs = {APM : {street : go.Bar(
                                x = times.loc[(times['corridor'] == street) & (times['mon'] <= middate) & (times['time_period'] == APM)].groupby(['dir'])['travel_time'].mean().index,
                                y = times.loc[(times['corridor'] == street) & (times['mon'] <= middate) & (times['time_period'] == APM)].groupby(['dir'])['travel_time'].mean(),
                                name = 'Before',
                                marker = dict(color = 'rgb(0,58,114)'), #bar color. Also accepts list of colors corresponding to each column
                                width = .3)
    
                                for street in streets} for APM in ('AM', 'PM')}

after_figs = {APM : {street :go.Bar(
                                x = times.loc[(times['corridor'] == street) & (times['mon'] >= middate) & (times['time_period'] == APM)].groupby(['dir'])['travel_time'].mean().index,
                                y = times.loc[(times['corridor'] == street) & (times['mon'] >= middate) & (times['time_period'] == APM)].groupby(['dir'])['travel_time'].mean(),
                                name = 'After',
                                marker = dict(color = 'rgb(200,114,58)'), #bar color. Also accepts list of colors corresponding to each column
                                width = .3)

                                for street in streets} for APM in ('AM', 'PM')}


app.layout = html.Div([
                core.RadioItems(
                    id = 'AMPM',
                    options=[{'label' : timebucket, 'value' : timebucket} for timebucket in times['time_period'].unique()],
                    value = 'AM'
                    ),
                
                html.Span(
                        [core.Graph(id = streets[0]),
                         core.Graph(id = streets[1]),
                         core.Graph(id = streets[2])],
                         className = 'four columns'
                         ),
                html.Span(
                        [core.Graph(id = streets[3]),
                         core.Graph(id = streets[4]),
                         core.Graph(id = streets[5])],
                         className = 'four columns'
                         )
                ])
app.css.append_css({
    "external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"
})
#interactivity
@app.callback(

    dash.dependencies.Output(streets[0], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_dundas(AMPM):
    return getfig(streets[0], AMPM)

@app.callback(

    dash.dependencies.Output(streets[1], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_queen(AMPM):
    return getfig(streets[1], AMPM)

@app.callback(

    dash.dependencies.Output(streets[2], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_adelaide(AMPM):
    return getfig(streets[2], AMPM)

@app.callback(

    dash.dependencies.Output(streets[3], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_front(AMPM):
    return getfig(streets[3], AMPM)

@app.callback(

    dash.dependencies.Output(streets[4], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_richmond(AMPM):
    return getfig(streets[4], AMPM)

@app.callback(

    dash.dependencies.Output(streets[5], 'figure'),
    [dash.dependencies.Input('AMPM', 'value')])
def update_wellington(AMPM):
    return getfig(streets[5], AMPM)



if __name__ == '__main__':
    app.run_server(debug=True)

