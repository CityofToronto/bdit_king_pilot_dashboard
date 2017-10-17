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

beforeafter = pandasql.read_sql(SQL, con)
children = []

beforedate = date(2017, 10, 1)
afterdate = date(2017, 11, 1)
street = 'Dundas'

before = beforeafter.loc[(beforeafter['corridor'] == street) & (beforeafter['mon'] == beforedate)]
after = beforeafter.loc[(beforeafter['corridor'] == street) & (beforeafter['mon'] == afterdate)]

fig1_1 = go.Bar(x = before['dir'],
              y = before['travel_time'],
              name = 'Before')

fig1_2 = go.Bar(x = after['dir'],
              y = after['travel_time'],
              name = 'After')

layout1 = go.Layout(barmode = 'group',
                   title = street,
                   xaxis = dict(title = 'Before/After'),
                   yaxis = dict(title = 'Travel Time'))

data = [fig1_1, fig1_2]

fig1 = go.Figure(data = data, layout = layout1)

children.append(core.Graph(id='testGraph1', figure = fig1))

street = 'Queen'

before = beforeafter.loc[(beforeafter['corridor'] == street) & (beforeafter['mon'] == beforedate)]
after = beforeafter.loc[(beforeafter['corridor'] == street) & (beforeafter['mon'] == afterdate)]

fig2_1 = go.Bar(x = before['dir'],
              y = before['travel_time'],
              name = 'Before')

fig2_2 = go.Bar(x = after['dir'],
              y = after['travel_time'],
              name = 'After')

layout2 = go.Layout(barmode = 'group',
                   title = street,
                   xaxis = dict(title = 'Before/After'),
                   yaxis = dict(title = 'Travel Time'))


data = [fig1_1, fig1_2]

fig2 = go.Figure(data = data, layout = layout2)

children.append(core.Graph(id='testGraph2', figure = fig2))

app = dash.Dash()

app.layout = html.Div([html.Div(children[0]),
                       html.Div(children[1])])



if __name__ == '__main__':
    app.run_server(debug=True)