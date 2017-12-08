import dash_components
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import calendar
from datetime import date, datetime
import json
import os
from flask import send_from_directory

streetcar_df = pd.read_csv('streetcar_travel_times.csv')


###################################################################################################
#                                                                                                 #
#                                        Constants                                                #
#                                                                                                 #
###################################################################################################

# Data management constants
# Streetcar speeds table
TIME_PERIODS = ['AM', 'PM']
MONTHS = pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month).unique()

# Dashboard appearance
TITLE = 'King Street Transit Pilot: Dashboard'
MAIN_DIV = 'main-page'
AM_PEAK_LABEL = 'AM PEAK PERIOD (7-10AM)'
PM_PEAK_LABEL = 'PM PEAK PERIOD (4-7PM)'

###################################################################################################
#                                                                                                 #
#                                   Data Manipulation                                             #
#                                                                                                 #
###################################################################################################


# Data for streetcar table
def filter_sc_table_data(month, period):
	filtered = streetcar_df[(pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month)==month) & (streetcar_df['time_period']==period)]
	filtered_json = json.loads(filtered.to_json(orient='records'))
	return filtered_json


###################################################################################################
#                                                                                                 #
#                                         App Layout                                              #
#                                                                                                 #
###################################################################################################

app = dash.Dash('')

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server

app.layout = html.Div(children=[
                            html.Link(
                                rel='stylesheet',
                                href='/src/css/dashboard.css'
                            ),
                            html.Link(
                                rel='stylesheet',
                                href='/src/css/style.css'
                            ),
                            html.Link(
                                rel='stylesheet',
                                href='/src/css/SCStable.css'
                            ),
							html.H2(children='AVERAGE STREETCAR TRAVEL TIME'),
							html.Div(children=[
								html.H3(children=AM_PEAK_LABEL),
								dash_components.StreetcarSpeeds( id='am-scs-table', data=filter_sc_table_data(9, 'AM')),
							], className='four columns'),
							html.Div(children=[
								html.H3(children=PM_PEAK_LABEL),
								dash_components.StreetcarSpeeds( id='pm-scs-table', data=filter_sc_table_data(9, 'PM')),
							], className='four columns'),
                        dcc.RadioItems(
							id='streetcar-month-radio',
							options = [{'label': calendar.month_abbr[i], 'value': i} for i in MONTHS],
							value=MONTHS[0],
							labelStyle={'display': 'inline-block'}
						    )
						])

################################CSS Loader###########################################

@app.server.route('/src/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'src')
    return send_from_directory(static_folder, path)

###################################################################################################
#                                                                                                 #
#                                         Controllers                                             #
#                                                                                                 #
###################################################################################################	

@app.callback(
	dash.dependencies.Output('am-scs-table', 'data'),
	[dash.dependencies.Input('streetcar-month-radio', 'value')])
def update_am_scs_scstable(current_month, current_period='AM'):
    filtered_data = filter_sc_table_data(current_month, current_period)
    return filtered_data

@app.callback(
	dash.dependencies.Output('pm-scs-table', 'data'),
	[dash.dependencies.Input('streetcar-month-radio', 'value')])
def update_pm_scs_scstable( current_month, current_period='PM'):
    filtered_data = filter_sc_table_data(current_month, current_period)
    print('Update PM Table')
    print(filtered_data)
    return filtered_data

if __name__ == '__main__':
    app.run_server(debug=True)
