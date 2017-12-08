import dash_components
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import calendar
import json
import os
from flask import send_from_directory

streetcar_df = pd.read_csv('streetcar_travel_times.csv')

street_volumes_df = pd.read_csv('street_volumes.csv')
street_segments_df = pd.read_csv('streets_segments31.csv')
streetlines_df = pd.read_csv('streets_lines3.csv')

###################################################################################################
#                                                                                                 #
#                                        Constants                                                #
#                                                                                                 #
###################################################################################################

# Data management constants
TIME_PERIODS = ['AM', 'PM']
MONTHS = pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month).unique()

# Dashboard appearance
TITLE = 'King Street Transit Pilot: Dashboard'

app = dash.Dash('')

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

#layout
app.layout = html.Div([
	html.Link(
		rel='stylesheet',
		href='/src/css/SCStable.css'
	),
	html.Div(
	dash_components.StreetcarSpeeds(id='streetcarspeeds', div_class='scscontainer', data=json.loads(streetcar_df[(pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month)==9) & (streetcar_df['time_period']=='AM')].to_json(orient='records')))
	),
	html.Div(
	dash_components.VolumeMap(id='volumemap', sl_data=json.loads(streetlines_df.to_json(orient='records')),
												ss_data=json.loads(street_segments_df.to_json(orient='records')),
												volume_data=json.loads(street_volumes_df[(pd.to_datetime(street_volumes_df['mon']).map(lambda t: t.date().month)==11) & (street_volumes_df['time_period']=='AM')].to_json(orient='records')))
	),
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

@app.server.route('/src/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'src')
    return send_from_directory(static_folder, path)


# Update StreetCarSpeeds table when period_radio or month_radio value changes
@app.callback(
	dash.dependencies.Output('streetcarspeeds', 'data'),
	[dash.dependencies.Input('period_radio', 'value'),
	 dash.dependencies.Input('month_radio', 'value')])
def update_scstable(current_period, current_month):
	tt_subset = streetcar_df[(pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month)==current_month) & (streetcar_df['time_period']==current_period)]
	return json.loads(tt_subset.to_json(orient='records'))

if __name__ == '__main__':
    app.run_server(debug=True)
