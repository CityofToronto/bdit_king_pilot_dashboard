import dash_components
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import calendar
import json
import os
from flask import send_from_directory

df = pd.read_csv('streetcar_travel_times.csv')

###################################################################################################
#                                                                                                 #
#                                        Constants                                                #
#                                                                                                 #
###################################################################################################

# Data management constants
TIME_PERIODS = ['AM', 'PM']
MONTHS = pd.to_datetime(df['mon']).map(lambda t: t.date().month).unique()

# Dashboard appearance
TITLE = 'King Street Transit Pilot: Dashboard'

app = dash.Dash('')

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server

#layout
app.layout = html.Div([
	html.Link(
		rel='stylesheet',
		href='/src/css/dashboard.css'
	),
	html.Link(
		rel='stylesheet',
		href='/src/css/style.css'
	),
	html.Div(children=[
		html.H1(children=TITLE, id='title')
	], className='row twelve columns'),
	html.Div(children=[
		html.H2(id='streetcarspeedDiv', children='Weekday AM Peak'),
		html.Div(children=[
			dash_components.StreetcarSpeeds( id='streetcarspeeds', data=json.loads(df[(pd.to_datetime(df['mon']).map(lambda t: t.date().month)==9) & (df['time_period']=='AM')].to_json(orient='records'))),
			dash_components.StreetcarSpeeds( id='streetcarspeeds', data=json.loads(df[(pd.to_datetime(df['mon']).map(lambda t: t.date().month)==9) & (df['time_period']=='AM')].to_json(orient='records')))
		]),
		html.Div(children=[
			dash_components.StreetcarSpeeds( id='streetcarspeeds', data=json.loads(df[(pd.to_datetime(df['mon']).map(lambda t: t.date().month)==9) & (df['time_period']=='AM')].to_json(orient='records'))),
			dash_components.StreetcarSpeeds( id='streetcarspeeds', data=json.loads(df[(pd.to_datetime(df['mon']).map(lambda t: t.date().month)==9) & (df['time_period']=='AM')].to_json(orient='records')))
		])
	], className='row twelve columns'),
	dcc.RadioItems(
		id='period_radio',
		options = [{'label': i, 'value': i} for i in TIME_PERIODS],
		value=TIME_PERIODS[0],
		labelStyle={'display': 'inline-block'}
	),
	dcc.RadioItems(
		id='month_radio',
		options = [{'label': calendar.month_abbr[i], 'value': i} for i in MONTHS],
		value=MONTHS[0],
		labelStyle={'display': 'inline-block'}
	)
])

@app.server.route('/src/css/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'src')
    return send_from_directory(static_folder, path)


# Update StreetCarSpeeds table when period_radio or month_radio value changes
@app.callback(
	dash.dependencies.Output('streetcarspeeds', 'data'),
	[dash.dependencies.Input('period_radio', 'value'),
	 dash.dependencies.Input('month_radio', 'value')])
def update_scstable(current_period, current_month):
	tt_subset = df[(pd.to_datetime(df['mon']).map(lambda t: t.date().month)==current_month) & (df['time_period']==current_period)]
	return json.loads(tt_subset.to_json(orient='records'))

if __name__ == '__main__':
    app.run_server(debug=True)
