# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 09:39:25 2017

@author: rrodger
"""

from psycopg2 import connect
import pandas.io.sql as pandasql
import configparser
from datetime import date, timedelta
import dash
import dash_core_components as core
import dash_html_components as html
import plotly.graph_objs as go
#from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

CONFIG = configparser.ConfigParser()
CONFIG.read('C:\\Users\\rrodger\\reed.cfg')
dbset = CONFIG['DBSETTINGS']
con = connect(**dbset)

SQL = '''SELECT corridor, dir, mon, avg(tt.tavel_time) as travel_time
FROM dbs_travel_times tt
GROUP BY corridor, dir, mon'''

times = pandasql.read_sql(SQL, con)

middate = date(2017, 10, 2)

streets = ['Dundas', 'Queen']

def getFig(street, midDate, times): #returns a graph_objs figure from a dataset.
#can be stacked/grouped if data is appropriately formatted.
    before = times.loc[(times['corridor'] == street) & (times['mon'] <= middate)]
    after = times.loc[(times['corridor'] == street) & (times['mon'] >= middate)]
    
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


#Generates a list of graphs in divs for each street in a list.

graphdivs = [html.Div(core.Graph(id = ('traveltime_' + street), figure = getFig(street, middate, times))) for street in streets] #, core.Graph(id = ('traveltime_' + streets[1]), figure = figures[1])]
app.layout = html.Div([core.RadioItems(
                id = 'streetname',
                options=[{'label' : timebucket, 'value' : timebucket} for timebucket in ('AM','PM')],
                value = 'AM'),
                html.Div(graphdivs)])


if __name__ == '__main__':
    app.run_server(debug=True)