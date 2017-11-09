import json
import os
from collections import OrderedDict

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

DATA = pd.read_csv("data/daily_fake.csv")
BASELINE = pd.read_csv("data/baselines_fake.csv")

STREETS = ['Dundas', 'Queen', 'Adelaide', 'Richmond', 'Wellington', 'Front']
DIRECTIONS = sorted(BASELINE['direction'].unique())
TIMEPERIODS = BASELINE[['day_type','period']].drop_duplicates()
THRESHOLD = 1

STATE_DIV_ID = 'clicks-storage'
SELECTED_STREET_DIV = 'selected-street'
TABLE_DIV_ID = 'div-table'
TIMEPERIOD_DIV = 'timeperiod'
CONTROLS = dict(timeperiods='timeperiod-radio',
                day_types='day-type-radio')
GRAPHS = ['eb_graph', 'wb_graph']

def generate_row_class(clicked):
    '''Assigns class to clicked row'''
    if clicked:
        return 'selected'
    else:
        return 'notselected'

def generate_direction_cells(before, after):
    return [html.Td(after, className=after_cell_class(before, after)),
            html.Td(before, className='baseline')]

def after_cell_class(before, after):
    if after - before > THRESHOLD:
        return 'worse'
    elif after - before < -THRESHOLD:
        return 'better'
    else:
        return 'same'

def generate_row(df_row, baseline_row, row_state):
    '''Create an HTML row from a database row
    '''
    return html.Tr([html.Td(df_row.street, className='segname'),
                    *generate_direction_cells(baseline_row.EB, df_row.EB),
                    *generate_direction_cells(baseline_row.WB, df_row.WB)],
                   id=df_row.street,
                   className=generate_row_class(row_state['clicked']),
                   n_clicks=row_state['n_clicks'])

app = dash.Dash()
app.config['suppress_callback_exceptions']=True
server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

INITIAL_STATE = OrderedDict([(street,
                              dict(n_clicks=(1 if street == 'Dundas' else 0),
                                   clicked=(street == 'Dundas'))) for street in STREETS])

def deserialise_state(clicks_json):
    return json.loads(clicks_json, object_pairs_hook=OrderedDict)

def serialise_state(clicks_dict):
    return json.dumps(clicks_dict)

def pivot_order(df):
    pivoted = df.pivot_table(index='street', columns='direction', values='tt').reset_index()
    pivoted.street = pivoted.street.astype("category")
    pivoted.street.cat.set_categories(STREETS, inplace=True)
    return pivoted.sort_values(['street']).round(1)

def filter_table_data(period, day_type):
    '''Return data aggregated and filtered by period
    '''
    #current data
    filtered = DATA[(DATA['period'] == period) &
                    (DATA['day_type'] == day_type)].groupby(by=['street',
                                                                'direction'],
                                                            as_index=False).mean()
    pivoted = pivot_order(filtered)

    #baseline data

    filtered_baseline = BASELINE[(BASELINE['period'] == period) & (BASELINE['day_type'] == day_type)]
    pivoted_baseline = pivot_order(filtered_baseline)

    return (pivoted, pivoted_baseline)

def filter_graph_data(street, direction, day_type='Weekday', period='AMPK'):
    '''Filter dataframes by street, direction, day_type, and period
    Returns a filtered baseline, and a filtered current dataframe
    '''
    filtered = DATA[(DATA['street'] == street) &
                    (DATA['period'] == period) &
                    (DATA['day_type'] == day_type) &
                    (DATA['direction'] == direction)]
    filtered_baseline = BASELINE[(BASELINE['street'] == street) &
                                 (BASELINE['period'] == period) &
                                 (BASELINE['day_type'] == day_type) &
                                 (BASELINE['direction'] == direction)]
    return (filtered, filtered_baseline)

def generate_graph(street, direction, day_type='Weekday', period='AMPK'):
    after_data, base_data = filter_graph_data(street, direction, day_type, period)
    data = [go.Bar(x=after_data['date'],
                   y=after_data['tt'])]
    line = None
    min_date, max_date = after_data.date.min(), after_data.date.max()
    if not base_data.empty:
        line = {'type':'line',
            'x0': 0,
            'x1': 1,
            'xref': 'paper',
            'y0': base_data.iloc[0]['tt'],
            'y1': base_data.iloc[0]['tt'],
            'line': {'color': 'rgba(128, 128, 128, 0.7)',
                     'width': 4}
        }
    layout = dict(title=direction,
                  xaxis=dict(title='Date'),
                  yaxis=dict(title='Travel Time (min)'),
                  shapes=[line])
    return {'layout': layout, 'data': data}

app.layout = html.Div([
html.Div(children=[html.H1(children='King Street Pilot', id='title'),
                  ], className='row twelve columns'),
    html.Div([
        html.Div(children=[
            html.H2(id=TIMEPERIOD_DIV, children='AM Peak Travel Times'),
            html.H2('Bathurst - Jarvis'),
            html.Div(id=TABLE_DIV_ID),
            dcc.RadioItems(id=CONTROLS['timeperiods'],
                           value=TIMEPERIODS.iloc[0]['period']),
            dcc.RadioItems(id=CONTROLS['day_types'],
                           options=[{'label': day_type, 'value': day_type} for day_type in TIMEPERIODS['day_type'].unique()],
                           value=TIMEPERIODS.iloc[0]['day_type'])
                           ],
                 className='four columns'
                ),
        html.Div(children=[
            dcc.Graph(id=GRAPHS[0], figure=generate_graph(STREETS[0], 'EB')),
            dcc.Graph(id=GRAPHS[1], figure=generate_graph(STREETS[0], 'WB'))
        ],
                 className='eight columns'
                ),
    ], className='row'),
    html.Div(id=STATE_DIV_ID, style={'display': 'none'}, children=serialise_state(INITIAL_STATE)),
    html.Div(id=SELECTED_STREET_DIV, style={'display': 'none'}, children=[STREETS[0]])
    ])

@app.callback(Output(CONTROLS['timeperiods'], 'options'),
              [Input(CONTROLS['day_types'], 'value')])
def generate_radio_options(day_type = 'Weekday'):
    return [{'label': period, 'value': period} for period in TIMEPERIODS[TIMEPERIODS['day_type'] == day_type]['period']]

@app.callback(Output(CONTROLS['timeperiods'], 'value'),
              [Input(CONTROLS['day_types'], 'value')])
def generate_radio_options(day_type = 'Weekday'):
    return TIMEPERIODS[TIMEPERIODS['day_type'] == day_type].iloc[0]['period']

@app.callback(Output(TABLE_DIV_ID, 'children'),
              [Input(CONTROLS['timeperiods'], 'value'),
               Input(CONTROLS['day_types'], 'value')],
              [State(STATE_DIV_ID, 'children')])
def generate_table(period, day_type, state_data):
    state_data_dict = deserialise_state(state_data)
    filtered_data, baseline = filter_table_data(period, day_type)
    return html.Table([html.Tr([html.Td(""), html.Td("Eastbound", colSpan=2), html.Td("Westbound", colSpan=2)])] +
                      [html.Tr([html.Td(""), html.Td("After"), html.Td("Baseline"), html.Td("After"), html.Td("Baseline")])] +
                      [generate_row(new_row, baseline_row, row_state)
                       for new_row, baseline_row, row_state
                       in zip(filtered_data.itertuples(),
                              baseline.itertuples(),
                              state_data_dict.values())]
                      , id='data_table')


def create_row_click_function(streetname):
    '''Create a callback function for a given streetname
    streetname is the id for the row in the datatable

    '''
    @app.callback(Output(streetname, 'className'),
                  [Input(SELECTED_STREET_DIV, 'children')])
    def update_clicked_row(street):
        '''Inner function to update row with id=streetname
        '''
        if street:
            return generate_row_class(streetname ==  street[0])
        else:
            return generate_row_class(False)
    update_clicked_row.__name__ = 'update_row_'+streetname
    return update_clicked_row

[create_row_click_function(key) for key in INITIAL_STATE.keys()]

@app.callback(Output(STATE_DIV_ID, 'children'),
              [Input(street, 'n_clicks') for street in STREETS],
              [State(STATE_DIV_ID, 'children'), 
               State(SELECTED_STREET_DIV, 'children')] )
def button_click(*args):
    rows, old_clicks, prev_clicked_street = args[:-1], args[-2], args[-1]
    clicks = deserialise_state(old_clicks)
    click_updated = False
    for click_obj, n_click_new in zip(clicks.values(), rows):
        if n_click_new > click_obj['n_clicks']:
            click_obj['clicked'] = True
            click_obj['n_clicks'] = n_click_new
            click_updated = True
        else:
            click_obj['clicked'] = False
    #If no street was found to be clicked by this function, revert to previously clicked street.
    if not click_updated:
        clicks[prev_clicked_street[0]]['clicked'] = True
    return serialise_state(clicks)

@app.callback(Output(SELECTED_STREET_DIV, 'children'),
              [Input(STATE_DIV_ID, 'children')])
def update_selected_street(state_data):
    state_data_dict = deserialise_state(state_data)
    return [street for street, click_obj in state_data_dict.items() if click_obj['clicked']]

def create_update_graph(graph_number):
    @app.callback(Output(GRAPHS[graph_number], 'figure'),
                  [Input(SELECTED_STREET_DIV, 'children'),
                   Input(CONTROLS['timeperiods'], 'value'),
                   Input(CONTROLS['day_types'], 'value')])
    def update_graph(street, period, day_type):
        return generate_graph(street[0], DIRECTIONS[graph_number], period=period, day_type=day_type)
    update_graph.__name__ = 'update_graph_' + GRAPHS[graph_number]
    return update_graph

[create_update_graph(i) for i in range(len(GRAPHS))]

@app.callback(Output(TIMEPERIOD_DIV, 'children'),
              [Input(CONTROLS['timeperiods'], 'value'),
               Input(CONTROLS['day_types'], 'value')])
def update_timeperiod(timeperiod, day_type):
    return day_type + ' ' + timeperiod + ' Travel Times'


app.css.append_css({
    'external_url': 'https://cityoftoronto.github.io/bdit_king_pilot_dashboard/css/dashboard.css'
})
    
if __name__ == '__main__':
    app.run_server(debug=True)
