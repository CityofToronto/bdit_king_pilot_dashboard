import os
import struct

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas
import plotly.graph_objs as go

app = dash.Dash()
# In case there are problems with react loading from unpkg, set to True
app.css.config.serve_locally = False
app.scripts.config.serve_locally = False

server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')


NORMAL_TRAVEL_TIMES = dict(AM=dict(WB=dict(min_tt=20,
                                           max_tt=23),
                                   EB=dict(min_tt=22,
                                           max_tt=25)))
streetcar_df = pandas.read_csv('data/streetcar_travel_times.csv')

MIN_DATE, MAX_DATE = streetcar_df.mon.min(), streetcar_df.mon.max()

HEX_COLOURS = dict(WB='ff5b33',
                   EB='a97bc4')

COLOURS = {}
#convert HEX colours to rgb strings e.g.: '255,91,51'
for direction, colour in HEX_COLOURS.items():
    rgb_colour = struct.unpack('BBB', bytes.fromhex(colour) )
    COLOURS[direction] = ','.join([str(val) for val in rgb_colour])


def filter_aggregate_timeperiod(timeperiod: str):
    """
    Returns the dataframe filtered by the provided timeperiod
        :param timeperiod:
    """
    filtered = streetcar_df[streetcar_df['time_period'] == timeperiod]
    agged_df = filtered[['mon',
                      'dir',
                      'travel_time']].groupby(['mon',
                                               'dir'],
                                              as_index=False).sum()
    return agged_df

def create_shapes(timeperiod: str):
    shapes_lst = []
    alpha = '0.5'
    
    for _dir, y_extents in NORMAL_TRAVEL_TIMES[timeperiod].items():
        colour_str = COLOURS[_dir]
        rgba = 'rgba('+colour_str+','+alpha+')'
        shapes_lst.append({'type': 'rect',
                           'x0': MIN_DATE,
                           'y0': y_extents['min_tt'],
                           'x1': MAX_DATE,
                           'y1': y_extents['max_tt'],
                           'line':{
                               'color': rgba
                           },
                           'fillcolor': rgba
                           })
    return shapes_lst

def create_graph(agged_df, shapes_lst):
    agged_wb = agged_df[agged_df['dir'] == 'WB']
    agged_eb = agged_df[agged_df['dir'] == 'EB']

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
                  yaxis=dict(title="Travel Time (min)"),
                  shapes=shapes_lst)
    return {'layout': layout, 'data': data}

agged = filter_aggregate_timeperiod('AM')
shapes = create_shapes('AM')

app.layout = html.Div(children=[html.Div(dcc.Graph(id='travel-time-graph',
                                                   figure=create_graph(agged, shapes)))
                               ])

if __name__ == '__main__':
    app.run_server(debug=True)
