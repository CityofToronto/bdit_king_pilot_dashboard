from collections import OrderedDict

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

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
            ], className = 'row')

        ])

#Super critical to store in an OrderedDict
#This is a bad implementation, should be changed to a hidden div, see: https://community.plot.ly/t/app-not-resetting-with-page-refresh/5020/10
#https://plot.ly/dash/sharing-data-between-callbacks
CLICKS = OrderedDict([(df.iloc[i]['street'], 0) for i in range(len(df))])

@app.callback(Output('row-selected','children'),
              [Input(df.iloc[i]['street'], 'n_clicks') for i in range(len(df))] )
def button_click(*rows):
    global CLICKS
    state_clicked = ''
    n_clicks_clicked = 0
    for (state, n_click_old), n_click_new in zip(CLICKS.items(), rows):
        if n_click_new > n_click_old:
            state_clicked = state
            n_clicks_clicked = n_click_new
    
    CLICKS[state_clicked] = n_clicks_clicked
    return state_clicked

app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})
    
if __name__ == '__main__':
    app.run_server(debug=True)