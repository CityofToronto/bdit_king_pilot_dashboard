from collections import OrderedDict
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd

df = pd.read_csv("data/test.csv")

def generate_table(dataframe, max_rows=30):
    return html.Table(
        [
         html.Tr( [html.Td(""), html.Td("Eastbound",colSpan=2), html.Td("Westbound",colSpan=2)] )
        ] +
        [
         html.Tr( [html.Td(""), html.Td("After"), html.Td("Baseline"), html.Td("After"), html.Td("Baseline")] )
        ] +
        [html.Tr([
            html.Td(dataframe.iloc[i][col], id = dataframe.iloc[i]['street'] + col) for col in dataframe.columns
        ], id= dataframe.iloc[i]['street'], n_clicks=0) for i in range(min(len(dataframe), max_rows))]
        , id = 'data_table'
    )

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
                        generate_table(df),
                        html.Div(id='row-selected', children='Selected row')],
                    className='three columns'
                    ),
                html.Div(children=[
                        html.H2(children='Chart goes here')],
                    className='nine columns'
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
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})


    
if __name__ == '__main__':
    app.run_server(debug=True)