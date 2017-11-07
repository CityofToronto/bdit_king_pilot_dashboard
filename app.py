from collections import OrderedDict
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

DATA = pd.read_csv("data/test.csv")

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

def generate_row(df_row, row_state):
    '''Create an HTML row from a database row
    '''
    return html.Tr([
            html.Td(df_row.street, className = generate_cell_class(0)),
            html.Td(df_row.eb_after, className = generate_cell_class(1)),
            html.Td(df_row.eb_base, className = generate_cell_class(2)),
            html.Td(df_row.wb_after, className = generate_cell_class(3)),
            html.Td(df_row.wb_base, className = generate_cell_class(4))
        ], id= df_row.street, className = generate_row_class(row_state['clicked']), n_clicks=row_state['n_clicks']) 



app = dash.Dash()
app.config['suppress_callback_exceptions']=True
CLICKS = OrderedDict([( row.street, dict(n_clicks=0, clicked=(row.street=='Queen'))) for row in DATA.itertuples()])

def deserialise_clicks(clicks_json):
    return json.loads(clicks_json, object_pairs_hook=OrderedDict)

def serialise_clicks(clicks_dict):
    return json.dumps(clicks_dict)

def generate_table(state_data_dict):
    return html.Table(
           [html.Tr( [html.Td(""), html.Td("Eastbound",colSpan=2), html.Td("Westbound",colSpan=2)] )] +
           [html.Tr( [html.Td(""), html.Td("After"), html.Td("Baseline"), html.Td("After"), html.Td("Baseline")] )] +
           [generate_row(row, row_state) for row, row_state in zip(DATA.itertuples(), state_data_dict.values())]
        , id='data_table')

app.layout = html.Div([
#        html.Div(children=[
#            html.H1(children='King Street Pilot'),
#            ], className='row twelve columns'),
        
        html.Div([    
            html.Div(children=[
                        html.Div(id=TABLE_DIV_ID, children=generate_table(CLICKS))],
                    className='four columns'
                    ),
                html.Div(children=[
                        html.H2(id='row-selected', children='Selected row')],
                    className='eight columns'
                    ),
            ], className = 'row'),
        html.Div(id=HIDDEN_DIV_ID, style={'display': 'none'}, children=serialise_clicks(CLICKS))
        ])

def create_row_click_function(streetname):
    @app.callback(Output(streetname, 'className'),
                [Input(HIDDEN_DIV_ID, 'children')])
    def update_clicked_row(state_data):
        state_data_dict = deserialise_clicks(state_data)
        return generate_row_class(state_data_dict[streetname]['clicked'])
    update_clicked_row.__name__ = 'update_row_'+streetname
    return update_clicked_row

[create_row_click_function(key) for key in CLICKS.keys()]

@app.callback(Output(HIDDEN_DIV_ID,'children'),
              [Input(DATA.iloc[i]['street'], 'n_clicks') for i in range(len(DATA))],
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