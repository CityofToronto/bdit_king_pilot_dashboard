from collections import OrderedDict
import json
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

DATA = pd.read_csv("data/bt_king_fake_data.csv")
BASELINE = pd.read_csv("data/test.csv")

STREETS = BASELINE['street']
TIMEPERIODS = DATA['period'].unique()
HIDDEN_DIV_ID = 'clicks_storage'
TABLE_DIV_ID = 'div-table'

def generate_cell_class(colNum):
    if colNum == 0:
        return 'segname'
    else:
        return 'segother'
    
def generate_row_class(clicked):
    '''Assigns class to clicked row'''
    if clicked:
        return 'selected'
    else:
        return 'notselected'

def generate_row(df_row, baseline_row, row_state):
    '''Create an HTML row from a database row
    '''
    return html.Tr([
            html.Td(df_row.street, className = generate_cell_class(0)),
            html.Td(df_row.EB, className = generate_cell_class(1)),
            html.Td(baseline_row.eb_base, className = generate_cell_class(2)),
            html.Td(df_row.WB, className = generate_cell_class(3)),
            html.Td(baseline_row.wb_base, className = generate_cell_class(4))
        ], id= df_row.street, className = generate_row_class(row_state['clicked']), n_clicks=row_state['n_clicks']) 



app = dash.Dash()

server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')

INITIAL_STATE = OrderedDict([(street, dict(n_clicks=0, clicked=(street =='Queen'))) for street in STREETS])

def deserialise_clicks(clicks_json):
    return json.loads(clicks_json, object_pairs_hook=OrderedDict)

def serialise_clicks(clicks_dict):
    return json.dumps(clicks_dict)

def filter_data(timeperiod):
    '''Return data aggregated and filtered by timeperiod
    '''
    filtered = DATA[DATA['period']==timeperiod].groupby(by=['street','direction'], as_index=False).mean()
    pivoted = filtered.pivot_table(index='street', columns='direction', values='tt').reset_index()
    pivoted.street = pivoted.street.astype("category")
    pivoted.street.cat.set_categories(STREETS, inplace=True)
    return pivoted.sort_values(['street'])


def generate_table(state_data_dict, timeperiod = 'AMPK'):
    filtered_data = filter_data(timeperiod)
    return html.Table(
           [html.Tr( [html.Td(""), html.Td("Eastbound",colSpan=2), html.Td("Westbound",colSpan=2)] )] +
           [html.Tr( [html.Td(""), html.Td("After"), html.Td("Baseline"), html.Td("After"), html.Td("Baseline")] )] +
           [generate_row(new_row, baseline_row, row_state) for new_row, baseline_row, row_state in zip(filtered_data.itertuples(), BASELINE.itertuples(), state_data_dict.values())]
        , id='data_table')

app.layout = html.Div([
#        html.Div(children=[
#            html.H1(children='King Street Pilot'),
#            ], className='row twelve columns'),
        
        html.Div([    
            html.Div(children=[
                        html.Div(id=TABLE_DIV_ID, children=generate_table(INITIAL_STATE))],
                    className='four columns'
                    ),
                html.Div(children=[
                        html.H2(id='row-selected', children='Selected row')],
                    className='eight columns'
                    ),
            ], className = 'row'),
        html.Div(id=HIDDEN_DIV_ID, style={'display': 'none'}, children=serialise_clicks(INITIAL_STATE))
        ])

def create_row_click_function(streetname):
    '''Create a callback function for a given streetname
    streetname is the id for the row in the datatable

    '''
    @app.callback(Output(streetname, 'className'),
                [Input(HIDDEN_DIV_ID, 'children')])
    def update_clicked_row(state_data):
        '''Inner function to update row with id=streetname
        '''
        state_data_dict = deserialise_clicks(state_data)
        return generate_row_class(state_data_dict[streetname]['clicked'])
    update_clicked_row.__name__ = 'update_row_'+streetname
    return update_clicked_row

[create_row_click_function(key) for key in INITIAL_STATE.keys()]

@app.callback(Output(HIDDEN_DIV_ID,'children'),
              [Input(street, 'n_clicks') for street in STREETS],
              [State(HIDDEN_DIV_ID,'children')] )
def button_click(*args):
    rows, old_clicks = args[:-1], args[-1]
    clicks = deserialise_clicks(old_clicks)
    for (street_name, click_obj), n_click_new in zip(clicks.items(), rows):
        if n_click_new > click_obj['n_clicks']:
            click_obj['clicked'] = True
            click_obj['n_clicks'] = n_click_new
        else:
            click_obj['clicked'] = False   
    return serialise_clicks(clicks)

@app.callback(Output('row-selected', 'children'),
              [Input(HIDDEN_DIV_ID, 'children')])
def update_row_clicked(click_state):
    clicks = deserialise_clicks(click_state)
    return [street_name for street_name, click_obj in clicks.items() if click_obj['clicked']]

app.css.append_css({
    'external_url': 'https://cityoftoronto.github.io/bdit_king_pilot_dashboard/css/dashboard.css'
})


    
if __name__ == '__main__':
    app.run_server(debug=True)