import dash_components
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd
import calendar
import numpy as np
from datetime import date, datetime
import json
import os
from flask import send_from_directory

# Streetcar data
streetcar_df = pd.read_csv('streetcar_travel_times.csv')

# Car data # NEED MOCK DATA FOR BASELINE
car_df = pd.read_csv('car_travel_times.csv')
car_baseline_df = pd.read_csv('car_travel_times_baseline.csv')

# Car Volume Map data
street_volumes_df = pd.read_csv('street_volumes.csv')
street_segments_df = pd.read_csv('streets_segments31.csv')
street_lines_df = pd.read_csv('streets_lines3.csv')

# Headway reliability # MOCK DATA REPLACE WITH ACTUAL CSV LATER
baseline_headway_data = [{'id': 0, 'dir': 'EB', 'mon': '09/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 30},
			{'id': 1, 'dir': 'EB', 'mon': '10/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 22},
			{'id': 2, 'dir': 'WB', 'mon': '11/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 39},
			{'id': 3, 'dir': 'WB', 'mon': '12/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 42}]

headway_data = [{'id': 0, 'dir': 'EB', 'mon': '09/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 74},
			{'id': 1, 'dir': 'EB', 'mon': '09/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 72},
			{'id': 4, 'dir': 'WB', 'mon': '09/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 41},
			{'id': 5, 'dir': 'WB', 'mon': '09/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 26},
			{'id': 2, 'dir': 'EB', 'mon': '10/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 62},
			{'id': 3, 'dir': 'EB', 'mon': '10/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 45},
			{'id': 2, 'dir': 'WB', 'mon': '10/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 52},
			{'id': 3, 'dir': 'WB', 'mon': '10/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 62},
			{'id': 0, 'dir': 'EB', 'mon': '11/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 50},
			{'id': 1, 'dir': 'EB', 'mon': '11/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 74},
			{'id': 4, 'dir': 'WB', 'mon': '11/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 43},
			{'id': 5, 'dir': 'WB', 'mon': '11/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 36},
			{'id': 0, 'dir': 'EB', 'mon': '12/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 60},
			{'id': 1, 'dir': 'EB', 'mon': '12/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 70},
			{'id': 6, 'dir': 'WB', 'mon': '12/01/2017  12:00:00 AM', 'period': 'AM', 'hw': 52},
			{'id': 7, 'dir': 'WB', 'mon': '12/01/2017  12:00:00 AM', 'period': 'PM', 'hw': 76}]
baseline_headway_df = pd.DataFrame(baseline_headway_data)
headway_df = pd.DataFrame(headway_data)

###################################################################################################
#                                                                                                 #
#                                        Constants                                                #
#                                                                                                 #
###################################################################################################

# Data management constants
# Streetcar speeds table
TIME_PERIODS = ['AM', 'PM']
TIME_PERIOD_RADIO = [{'label': i, 'value': i} for i in TIME_PERIODS]

# Avaliable Month Filters
MONTHS = pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month).unique()
MONTH_RADIO = [{'label': calendar.month_name[i], 'value': i} for i in MONTHS]
MONTH_RADIO.append({'label': 'All', 'value': 13}) # 13 is used as the value to represent `All` or no month filter

# Default Filters
DEFAULT_MONTH = 13 # 'All'
DEFAULT_PERIOD = 'AM'

# Traffic flow graphs
STREETS = ['Dundas', 'Richmond', 'Wellington', 'Queen', 'Adelaide', 'Front']

YRNG = [0, car_df['travel_time'].max()] #All car travel time graphs have the same y axis

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

# Data for streetcar graph
def filter_sc_graph_data(period):
	streetcar_am = streetcar_df[streetcar_df['time_period'] == period]
	agged = streetcar_am[['mon','dir','travel_time']].groupby(['mon','dir'],as_index=False).sum() # Suppose to be overall mean (not currently in use)
	agged_wb = agged[agged['dir']=='WB']
	agged_eb = agged[agged['dir']=='EB']
	data = [go.Scatter(x=agged_wb['mon'], 
					y=agged_wb['travel_time'],
					mode='lines',
					name='WB'),
		go.Scatter(x=agged_eb['mon'],
					y=agged_eb['travel_time'],
					mode='lines',
					name='EB')]
	return data

# Data for streetcar table
def filter_sc_table_data(month, period):
	# Case if all data
	if (month == 13):
		filtered = streetcar_df[(streetcar_df['time_period']==period)].groupby(['segment_id', 'segment', 'dir'],as_index=False).mean()
	else:
		filtered = streetcar_df[(pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month)==month) & (streetcar_df['time_period']==period)]
	filtered_json = json.loads(filtered.to_json(orient='records'))
	return filtered_json

# Data for volume map
def filter_vol_data(month, period):
	# Case if all data
	if (month == 13):
		filtered = street_volumes_df[(street_volumes_df['time_period']==period)].groupby(['segment'],as_index=False).mean()
	else:
		filtered = street_volumes_df[(pd.to_datetime(street_volumes_df['mon']).map(lambda t: t.date().month)==month) & (street_volumes_df['time_period']==period)]
	filtered_json = json.loads(filtered.to_json(orient='records'))
	return filtered_json

# Data for Headway graph
def filter_hw_data(period, dir, month):
	baseline_data = baseline_headway_df[(baseline_headway_df['dir']==dir) & (baseline_headway_df['period']==period)]
	# Case if all data
	if (month == 13):
		data = headway_df[(headway_df['dir']==dir) & (headway_df['period']==period)].groupby(['mon','dir','period'],as_index=False).mean()
	else:
		data = headway_df[(headway_df['dir']==dir) & (headway_df['period']==period) & (pd.to_datetime(headway_df['mon']).map(lambda t: t.date().month)==month)]
	combined_data = [baseline_data, data]
	return combined_data

# Data for Car Travel Time graph
def filter_ctt_data(street, period, month):
	# Case if all data
	if (month == 13):
		current_data = car_df[(car_df['corridor'] == street) & (car_df['time_period'] == period)].groupby(['dir'],as_index=False)['travel_time'].mean()
	else:
		current_data = car_df[(car_df['corridor'] == street) & (pd.to_datetime(car_df['mon']).map(lambda t: t.date().month)==month) & (car_df['time_period'] == period)].groupby(['dir'],as_index=False)['travel_time'].mean()
	baseline_data = car_baseline_df[(car_baseline_df['corridor'] == street) & (car_baseline_df['time_period'] == period)].groupby(['dir'],as_index=False)['travel_time'].mean()
	y_current = []
	y_baseline = []
	# Convert dataframes to more manageable arrays
	# All graphs have before/after EB and before/after WB even if it is one way
	if any(current_data['dir'] == 'EB') and any(current_data['dir'] == 'WB'):
		y_current = current_data['travel_time'].values
		y_baseline = baseline_data['travel_time'].values
	elif any(current_data['dir'] == 'EB'):
		y_current = current_data['travel_time'].values
		y_current = np.append(y_current, 0) # Null current WB value
		y_baseline = baseline_data['travel_time'].values
		y_baseline = np.append(y_baseline, 0) # Null baseline WB value
	elif any(current_data['dir'] == 'WB'):
		y_current = current_data['travel_time'].values
		y_current = np.append(0, y_current) # Null current EB value
		y_baseline = baseline_data['travel_time'].values
		y_baseline = np.append(0, y_baseline) # Null baseline EB value
	
	x_label = ['EASTBOUND', 'WESTBOUND'] # x axis value/label
	before_data = go.Bar(
				x = x_label,
				y = y_baseline,
				text = ['%.0f' % elem for elem in y_baseline], # round decimal value
				textfont = dict(size=15, color='white'),
				textposition = 'inside',
				name = 'Before',
				marker = dict(color = 'rgba(255,165,0, 0.6)'),
				width = .3
	)
	after_data = go.Bar(
				x = x_label,
				y = y_current,
				text = ['%.0f' % elem for elem in y_current],
				textfont = dict(size=15, color='white'),
				textposition = 'inside',
				name = 'After',
				marker = dict(color = 'rgba(30,144,255, 0.6)'),
				width = .3
	)
	data = [before_data, after_data]
	return data

###################################################################################################
#                                                                                                 #
#                                         App Layout                                              #
#                                                                                                 #
###################################################################################################

# Streetcar graph
def generate_sc_graph(period):
	data = filter_sc_graph_data(period)
	layout = dict(title = period + ' TRAVEL TIMES', titlefont = dict(size=14),
			xaxis = dict(title="MONTH", titlefont = dict(size = 12), showline=True, showgrid=False, linecolor='black', linewidth=1, ticks='outside', tickfont = dict(size=10)),
            yaxis = dict(title="TRAVEL TIME (min)", titlefont = dict(size = 12), tickfont = dict(size=10)),
			autosize=True,
			height=250,
			margin=go.Margin(
				l=70,
				r=30,
				b=60,
				t=50,
				pad=4
			),
			showlegend=False)
	annotations = []
	# Annotation at the end of line to tell what line represent which direction
	annotations.append(dict(x=data[0].x.iloc[-1], y=data[0].y.iloc[-1], xanchor='left', yanchor='middle', text='WB', showarrow=False))
	annotations.append(dict(x=data[1].x.iloc[-1], y=data[1].y.iloc[-1], xanchor='left', yanchor='middle', text='EB', showarrow=False))
	layout['annotations'] = annotations
	figure = {'layout': layout, 'data': data}
	return figure

# Car traffic flow graph
def generate_tf_graph(street, period, month):
	data = filter_ctt_data(street, period, month)
	diffWB = int(data[0].y[1] - data[1].y[1])
	# Determine what is displayed above each direction
	# Represent difference between baseline and current data for each direction
	# WB difference
	if ((data[0].y[1] - data[1].y[1]) == 0):
		strdiffWB = '-'
	elif(diffWB > 0):
		strdiffWB = '+' + str(diffWB)+ ' min'
	elif(diffWB < 0):
		strdiffWB = str(diffWB) + ' min'
	else:
		strdiffWB = '< 1 min'
	# EB difference
	diffEB = int(data[0].y[0] - data[1].y[0])
	if ((data[0].y[0] - data[1].y[0]) == 0):
		strdiffEB = '-'
	elif(diffEB > 0):
		strdiffEB = '+' + str(diffEB)+ ' min'
	elif(diffEB < 0):
		strdiffEB = str(diffEB)+ ' min'
	else:
		strdiffEB = '< 1 min'
	
	layout = go.Layout(title = street.upper(), titlefont = dict(size = 14),
						xaxis = dict(title = 'DIRECTION', titlefont = dict(size = 12), tickfont = dict(size=10)),
						yaxis = dict(title = 'TRAVEL TIME', titlefont = dict(size = 12), range = YRNG, tickfont = dict(size=10)),
						autosize = True,
						height = 250,
						margin=go.Margin(
									l=40,
									r=0,
									b=35,
									t=50,
									pad=4
								),
						hovermode="closest",
						showlegend=False,
						legend=dict(x=0, y=-1.5, orientation="h"),
						annotations = [])
	layout['barmode'] = 'group'
	# Displays the difference above the respective bars
	layout['annotations'].append(dict(
									x = 'WESTBOUND',
									y = YRNG[1],
									text = strdiffWB,
									xanchor = 'centre',
									yref = 'top',
									showarrow = False,
									font = dict(color = "black", size = 16)))
	layout['annotations'].append(dict(x = 'EASTBOUND',
									y = YRNG[1],
									text = strdiffEB,
									xanchor = 'centre',
									yref = 'top',
									showarrow = False,
									font = dict(color = "black", size = 16)))
	return {'data' : data, 'layout' : layout}

# Streetcar Headway Reliability graph
def generate_schr_graph(period, dir, mon):
	filtered_data = filter_hw_data(period, dir, mon)
	# Get baseline headway data
	baseline_data = filtered_data[0]
	before = baseline_data['hw'].values[0]
	# Get current headway data
	current_data = filtered_data[1]
	after = current_data['hw'].values[0]
	
	values = [before, after]
	# Values that are displayed inside the bar
	fmt_values = [str(before) + '%', str(after) + '%']
	labels = ['BEFORE', 'AFTER']
	data = [go.Bar(x=labels, y=values, text=fmt_values, textfont = dict(size=15, color='white'), textposition = 'inside', marker=dict(color=['rgba(255,165,0, 0.6)', 'rgba(30,144,255, 0.6)']))]
	layout = go.Layout(title = period + ' PEAK PERIOD', titlefont = dict(size=14),
			xaxis = dict(title = 'WESTBOUND' if dir == 'WB' else 'EASTBOUND', titlefont = dict(size=12), tickfont = dict(size=10)),
			yaxis = dict(title = 'RELIABILITY %', titlefont = dict(size = 12), range = [0, 100], tickfont = dict(size=10)),
			autosize = True,
			height = 250,
			margin=go.Margin(
						l=40,
						r=0,
						b=35,
						t=50,
						pad=4
					),
			hovermode="closest",
			showlegend=False,
			barmode = 'group')
	figure = {'layout': layout, 'data': data}
	return figure
	
app = dash.Dash('')

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

server = app.server

# main div contents
# Streetcar Tab
STREETCAR_LAYOUT = [html.Div(children=[
						html.Div(children=[
							# Average Streetcar Travel Time Section
							html.Div(children=[
								# Title
								html.Div(children=[
									html.H2(children='AVERAGE STREETCAR TRAVEL TIME', style={'margin-left':'0px'})
								], className='nine columns'),
								# AM Section
								html.Div(children=[
									html.H3(children=AM_PEAK_LABEL),
									dash_components.StreetcarSpeeds( id='am-baseline-scs-table', data=filter_sc_table_data(9, 'AM')), # Baseline scs table
									dash_components.StreetcarSpeeds( id='am-scs-table', data=filter_sc_table_data(DEFAULT_MONTH, 'AM')), # Current scs table
									html.Div(dcc.Graph(id='am-tt-graph', figure=generate_sc_graph('AM')), style={'border-style':'solid', 'border-width': '1px'}) # sctt graph
								], className='six columns'),
								# PM Section
								html.Div(children=[
									html.H3(children=PM_PEAK_LABEL),
									dash_components.StreetcarSpeeds( id='pm-baseline-scs-table', data=filter_sc_table_data(9, 'PM')), # Baseline scs table
									dash_components.StreetcarSpeeds( id='pm-scs-table', data=filter_sc_table_data(DEFAULT_MONTH, 'PM')), # Current scs table
									html.Div(dcc.Graph(id='pm-tt-graph', figure=generate_sc_graph('PM')), style={'border-style':'solid', 'border-width': '1px'}) # sctt graph
								], className='six columns')
							], className='nine columns', style={'margin-left':0}),
							# Streetcar Headway Reliability Section
							html.Div(children=[
								# Title
								html.Div(children=[
									html.H2(children='STREETCAR HEADWAY RELIABILITY', style={'margin-left':'0px'}),
									html.H4(children='% of streetcars within acceptable headway')
								], className='three columns'),
								# AM
								html.Div(children=[
									html.Div(dcc.Graph(id='am-wb-schr-graph', figure=generate_schr_graph('AM', 'WB', DEFAULT_MONTH))), # AM WB schr graph
									html.Div(dcc.Graph(id='am-eb-schr-graph', figure=generate_schr_graph('AM', 'EB', DEFAULT_MONTH)))  # AM EB schr graph
								], className='one-half columns'),
								# PM
								html.Div(children=[
									html.Div(dcc.Graph(id='pm-wb-schr-graph', figure=generate_schr_graph('PM', 'WB', DEFAULT_MONTH))), # PM WB schr graph
									html.Div(dcc.Graph(id='pm-eb-schr-graph', figure=generate_schr_graph('PM', 'EB', DEFAULT_MONTH)))  # PM EB schr graph
								], className='one-half columns')
							], className='three colums')
						], className='row'),
						# Period radio filters (not in use)
						# dcc.RadioItems(
							# id='streetcar-period-radio',
							# options = TIME_PERIOD_RADIO,
							# value=TIME_PERIODS[0],
							# className='radio-toolbar',
							# labelStyle={'display': 'inline-block'}
						# ),
						# Month radio filters
						dcc.RadioItems(
							id='streetcar-month-radio',
							options = MONTH_RADIO,
							value=DEFAULT_MONTH,
							className='radio-toolbar',
							labelStyle={'display': 'inline-block'}
						)]
					)]
# Car Tab
CAR_LAYOUT = [html.Div(children=[
				# Car Travel Time Section
				html.Div(children=[
					# Title
					html.Div(children=[
						html.H2(children='CAR TRAVEL TIME', style={'margin-left':'0px'})
					], className='column'),
					# Car Travel Time Graphs
					html.Div(children=[
						html.H3(id='ctt-peak-label', children=AM_PEAK_LABEL),
						html.Div(dcc.Graph(id = STREETS[0] + '-tf-graph'), # Dundas
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[1] + '-tf-graph'), # Richmond
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[2] + '-tf-graph'), # Wellington
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[3] + '-tf-graph'), # Queen
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[4] + '-tf-graph'), # Adelaide
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[5] + '-tf-graph'), # Front
								className='two columns')
					], className='row', style={'padding-left':'2%'})
				]),
				# Traffic Volume Section
				html.Div(children=[
						# Title
						html.H2(children='TRAFFIC VOLUMES', style={'margin-left':'0px'})
					], className='column'),
				# Volume Map
				html.Div(children=[
					html.Div(className='one columns'),
					html.Div(children=[
					dash_components.VolumeMap(id='volume-map', sl_data=json.loads(street_lines_df.to_json(orient='records')),
												ss_data=json.loads(street_segments_df.to_json(orient='records')),
												volume_data=filter_vol_data(DEFAULT_MONTH, DEFAULT_PERIOD))
					], className='ten columns'),
					html.Div(className='one columns')
				], className='row'),
				# Period radio filter
				dcc.RadioItems(
					id='car-period-radio',
					options = TIME_PERIOD_RADIO,
					value=DEFAULT_PERIOD,
					className='radio-toolbar',
					labelStyle={'display': 'inline-block'}
				),
				# Month radio filter
				dcc.RadioItems(
					id='car-month-radio',
					options = MONTH_RADIO,
					value=DEFAULT_MONTH,
					className='radio-toolbar',
					labelStyle={'display': 'inline-block'}
				)]
			)]

#layout
app.layout = html.Div([
	# Load style sheets
	# Dashboard
	html.Link(
		rel='stylesheet',
		href='/src/css/dashboard.css'
	),
	# Radio buttons etc
	html.Link(
		rel='stylesheet',
		href='/src/css/style.css'
	),
	# React Component specific
	html.Link(
		rel='stylesheet',
		href='/src/css/components.css'
	),
	# Title
	html.Div(children=[
		html.H1(children=TITLE, id='title')
	], className='row twelve columns'),
	# Tabs
	dcc.Tabs(tabs=[{'label': 'Streetcars', 'value': 'streetcar'},
					{'label': 'Cars', 'value': 'car'}],
					value='streetcar', id='tabs', style={'font-weight':'bold'}),
	# Main
	html.Div(id=MAIN_DIV, className='row', children=STREETCAR_LAYOUT), # Contents loaded via controllers. Default Streetcar tab.
	# Bottom footnote
	html.Div(children=html.H3(['Created by the ',
						html.A('Big Data Innovation Team',
						href="https://www1.toronto.ca/wps/portal/contentonly?vgnextoid=f98b551ed95ff410VgnVCM10000071d60f89RCRD")],
						style={'text-align':'right',
						'padding-right':'1em'}),
					className='row')
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

app.config['suppress_callback_exceptions']=True

# Tabs
@app.callback(Output('main-page', 'children'), [Input('tabs', 'value')])
def display_content(value):
	if value == 'streetcar':
		return STREETCAR_LAYOUT
	elif value == 'car':
		return CAR_LAYOUT

############## Streetcar tab ######################################################################

# Streetcar Speed tables controllers
# AM
@app.callback(
	Output('am-scs-table', 'data'),
	[Input('streetcar-month-radio', 'value')])
def update_am_scs_scstable(current_month):
	filtered_data = filter_sc_table_data(current_month, 'AM');
	return filtered_data
# PM
@app.callback(
	Output('pm-scs-table', 'data'),
	[Input('streetcar-month-radio', 'value')])
def update_pm_baseline_scstable(current_month):
	filtered_data = filter_sc_table_data(current_month, 'PM');
	return filtered_data

# Streetcar Headway Reliability controllers
# AM WB
@app.callback(
	Output('am-wb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_am_wb_schr_graph(current_month):
	figure = generate_schr_graph('AM', 'WB', current_month);
	return figure
# AM EB
@app.callback(
	Output('am-eb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_am_eb_schr_graph(current_month):
	figure = generate_schr_graph('AM', 'EB', current_month);
	return figure
# PM WB
@app.callback(
	Output('pm-wb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_pm_wb_schr_graph(current_month):
	figure = generate_schr_graph('PM', 'WB', current_month);
	return figure
# PM EB
@app.callback(
	Output('pm-eb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_pm_eb_schr_graph(current_month):
	figure = generate_schr_graph('PM', 'EB', current_month);
	return figure

################# Car tab ##########################################################################

# Updates the peak period label depending on current period
@app.callback(
    Output('ctt-peak-label', 'children'),
    [Input('car-period-radio', 'value')])
def update_tf_label(value):
	if value == 'AM':
		return AM_PEAK_LABEL
	elif value == 'PM':
		return PM_PEAK_LABEL
# Car Travel Time graph controllers
# Dundas
@app.callback(
    Output(STREETS[0] + '-tf-graph', 'figure'),
    [Input('car-month-radio', 'value'),
	Input('car-period-radio', 'value')])
def update_dundas(current_month, current_period):
    return generate_tf_graph(STREETS[0], current_period, current_month)
# Richmond
@app.callback(
	Output(STREETS[1] + '-tf-graph', 'figure'),
    [Input('car-month-radio', 'value'),
	Input('car-period-radio', 'value')])
def update_richmond(current_month, current_period):
    return generate_tf_graph(STREETS[1], current_period, current_month)	
# Wellington
@app.callback(
	Output(STREETS[2] + '-tf-graph', 'figure'),
    [Input('car-month-radio', 'value'),
	Input('car-period-radio', 'value')])
def update_wellington(current_month, current_period):
	return generate_tf_graph(STREETS[2], current_period, current_month)
# Queen
@app.callback(
    Output(STREETS[3] + '-tf-graph', 'figure'),
    [Input('car-month-radio', 'value'),
	Input('car-period-radio', 'value')])
def update_queen(current_month, current_period):
    return generate_tf_graph(STREETS[3], current_period, current_month)
# Adelaide
@app.callback(
    Output(STREETS[4] + '-tf-graph', 'figure'),
    [Input('car-month-radio', 'value'),
	Input('car-period-radio', 'value')])
def update_adelaide(current_month, current_period):
    return generate_tf_graph(STREETS[4], current_period, current_month)
# Front
@app.callback(
    Output(STREETS[5] + '-tf-graph', 'figure'),
    [Input('car-month-radio', 'value'),
	Input('car-period-radio', 'value')])
def update_front(current_month, current_period):
	return generate_tf_graph(STREETS[5], current_period, current_month)

# Volume Map controller
@app.callback(
	Output('volume-map', 'volume_data'),
    [Input('car-month-radio', 'value'),
	Input('car-period-radio', 'value')])
def update_vol_map(current_month, current_period):
	filtered_data = filter_vol_data(current_month, current_period);
	return filtered_data

if __name__ == '__main__':
    app.run_server(debug=True)
