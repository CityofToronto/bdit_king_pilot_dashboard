import os

import plotly.graph_objs as go
import pandas

import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()
# In case there are problems with react loading from unpkg, set to True
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False

server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

streetcar_df = pandas.read_csv('data/streetcar_travel_times.csv')

streetcar_am = streetcar_df[streetcar_df['time_period'] == 'AM']
agged = streetcar_am[['mon',
                      'dir',
                      'travel_time']].groupby(['mon',
                                               'dir'],
                                              as_index=False).sum()
agged_wb = agged[agged['dir'] == 'WB']
agged_eb = agged[agged['dir'] == 'EB']

data = [go.Scatter(x=agged_wb['mon'],
                   y=agged_wb['travel_time'],
                   mode='lines',
                   name='WB'),
        go.Scatter(x=agged_eb['mon'],
                   y=agged_eb['travel_time'],
                   mode='lines',
                   name='EB')
       ]
layout = dict(title='Average Streetcar Travel Times',
              xaxis=dict(title="Month"),
              yaxis=dict(title="Travel Time (min)"))

figure = {'layout': layout, 'data': data}
app.layout = html.Div(children=[html.Div(children=[html.Div(dcc.Graph(id='travel-time-graph',
                                                                      figure=figure))])
                               ])

if __name__ == '__main__':
    app.run_server(debug=True)
