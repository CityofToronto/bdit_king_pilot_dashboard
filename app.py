from collections import OrderedDict
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

df = pd.read_csv("data/test.csv")

def generate_cell_class(colNum):
    if colNum == 0:
        return 'segname'
    else:
        return 'segother'
    
def generate_row_class(selected_str, current_str):
    # if selected_str == current_str:
    if current_str == 'Queen':
        return 'selected';
    else:
        return 'notselected';

def generate_row(df_row, street_name = None):
    '''Create an HTML row from a database row
    '''
    return html.Tr([
            html.Td(df_row.street, className = generate_cell_class(0)),
            html.Td(df_row.eb_after, className = generate_cell_class(1)),
            html.Td(df_row.eb_base, className = generate_cell_class(2)),
            html.Td(df_row.wb_after, className = generate_cell_class(3)),
            html.Td(df_row.wb_base, className = generate_cell_class(4))
        ], id= df_row.street, className = generate_row_class(street_name, df_row.street), n_clicks=0) 

def generate_table(dataframe):
    return html.Table(
           [html.Tr( [html.Td(""), html.Td("Eastbound",colSpan=2), html.Td("Westbound",colSpan=2)] )] +
           [html.Tr( [html.Td(""), html.Td("After"), html.Td("Baseline"), html.Td("After"), html.Td("Baseline")] )] +
           [generate_row(row) for row in dataframe.itertuples()]
        , id='data_table')

app = dash.Dash()
CLICKS = OrderedDict([(df.iloc[i]['street'], dict(n_clicks=0, clicked=False)) for i in range(len(df))])



#Super critical to store in an OrderedDict
#This is a bad implementation, should be changed to a hidden div, see: https://community.plot.ly/t/app-not-resetting-with-page-refresh/5020/10
#https://plot.ly/dash/sharing-data-between-callbacks

def deserialise_clicks(clicks_json):
    return json.loads(clicks_json, object_pairs_hook=OrderedDict)

def serialise_clicks(clicks_dict):
    return json.dumps(clicks_dict)

app.layout = html.Div([
#        html.Div(children=[
#            html.H1(children='King Street Pilot'),
#            ], className='row twelve columns'),
        
        html.Div([    
            html.Div(children=[
                        html.Div(id='div-table', children=generate_table(df)),
                        html.Div(id='row-selected', children='Selected row')],
                    className='four columns'
                    ),
                html.Div(children=[
                        html.H2(children='Chart goes here')],
                    className='eight columns'
                    ),
            ], className = 'row'),
        html.Div(id='clicks_storage', style={'display': 'none'}, children=serialise_clicks(CLICKS))
        ])

@app.callback(Output('clicks_storage','children'),
              [Input(df.iloc[i]['street'], 'n_clicks') for i in range(len(df))],
              [State('clicks_storage','children')] )
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
              [Input('clicks_storage', 'children')])
def update_row_clicked(click_state):
    clicks = deserialise_clicks(click_state)
    return [street_name for street_name, click_obj in clicks.items() if click_obj['clicked']]

app.css.append_css({
    'external_url': 'https://cityoftoronto.github.io/bdit_king_pilot_dashboard/css/dashboard.css'
})


    
if __name__ == '__main__':
    app.run_server(debug=True)