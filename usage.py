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

# Streetcar data
streetcar_df = pd.read_csv('streetcar_travel_times.csv')
car_df = pd.read_csv('car_travel_times.csv')

# Car data # NEED MOCK DATA FOR BASELINE
car_df['mon'] = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S').date() for i in car_df['mon']]

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
MONTHS = pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month).unique()

# Traffic flow graphs
MIDDATE = date(2017, 10, 2)
STREETS = ['Dundas', 'Richmond', 'Wellington', 'Queen', 'Adelaide', 'Front']
BEFORE_FIGS = {period : {street : go.Bar(
								x = car_df.loc[(car_df['corridor'] == street) & (car_df['mon'] <= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean().index,
								y = car_df.loc[(car_df['corridor'] == street) & (car_df['mon'] <= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean(),
								name = 'Before',
								marker = dict(color = 'rgba(255,165,0, 0.6)'), #bar color. Also accepts list of colors corresponding to each column
								width = .3)
								for street in STREETS} for period in ('AM', 'PM')}
AFTER_FIGS = {period : {street : go.Bar(
								x = car_df.loc[(car_df['corridor'] == street) & (car_df['mon'] >= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean().index,
								y = car_df.loc[(car_df['corridor'] == street) & (car_df['mon'] >= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean(),
								name = 'After',
								marker = dict(color = 'rgba(30,144,255, 0.6)'), #bar color. Also accepts list of colors corresponding to each column
								width = .3)
								for street in STREETS} for period in ('AM', 'PM')}
YRNG = [0, car_df['travel_time'].max()] #All graphs have the same y axis

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
	agged = streetcar_am[['mon','dir','travel_time']].groupby(['mon','dir'],as_index=False).sum()
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
	filtered = streetcar_df[(pd.to_datetime(streetcar_df['mon']).map(lambda t: t.date().month)==month) & (streetcar_df['time_period']==period)]
	filtered_json = json.loads(filtered.to_json(orient='records'))
	return filtered_json

# Data for volume map
def filter_vol_data(month, period):
	filtered = street_volumes_df[(pd.to_datetime(street_volumes_df['mon']).map(lambda t: t.date().month)==month) & (street_volumes_df['time_period']==period)]
	filtered_json = json.loads(filtered.to_json(orient='records'))
	return filtered_json

def filter_hw_data(period, dir, month):
	baseline_data = baseline_headway_df[(baseline_headway_df['dir']==dir) & (baseline_headway_df['period']==period)]
	data = headway_df[(headway_df['dir']==dir) & (headway_df['period']==period) & (pd.to_datetime(headway_df['mon']).map(lambda t: t.date().month)==month)]
	combined_data = [baseline_data, data]
	return combined_data

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
	annotations.append(dict(x=data[0].x.iloc[-1], y=data[0].y.iloc[-1], xanchor='left', yanchor='middle', text='WB', showarrow=False))
	annotations.append(dict(x=data[1].x.iloc[-1], y=data[1].y.iloc[-1], xanchor='left', yanchor='middle', text='EB', showarrow=False))
	layout['annotations'] = annotations
	figure = {'layout': layout, 'data': data}
	return figure

# Car traffic flow graph
def generate_tf_graph(street, period):
    WB = False
    EB = False
    bdata = car_df[(car_df['corridor'] == street) & (car_df['mon'] <= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean()
    adata = car_df[(car_df['corridor'] == street) & (car_df['mon'] >= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean()
    if any('WB' == bdata.index):
        WB = True
        diffWB = int(bdata['WB'] - adata['WB'])
        
        if(diffWB > 0):
            strdiffWB = '+' + str(diffWB)+ ' min'
        elif(diffWB < 0):
            strdiffWB = str(diffWB) + ' min'
        else:
            strdiffWB = '< 1 min'
    if any('EB' == bdata.index):
        EB = True
        diffEB = int(bdata['EB'] - adata['EB'])
        
        if(diffEB > 0):
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
    if WB and EB:
        layout['barmode'] = 'group'
    if WB:
        layout['annotations'].append(dict(
                                        x = 'WB',
                                        y = YRNG[1],
                                        text = strdiffWB,
                                        xanchor = 'centre',
                                        yref = 'top',
                                        showarrow = False,
                                        font = dict(
                                               color = "black",
                                               size = 16,
                                               family = 'arial narrow')))
    if EB:
        layout['annotations'].append(dict(x = 'EB',
                                        y = YRNG[1],
                                        text = strdiffEB,
                                        xanchor = 'centre',
                                        yref = 'top',
                                        showarrow = False,
                                        font = dict(color = "black", size = 16, family = 'arial narrow')))
    return {'data' : [BEFORE_FIGS[period][street], AFTER_FIGS[period][street]], 'layout' : layout}

# Streetcar Headway Reliability graph
def generate_schr_graph(period, dir, mon):
	filtered_data = filter_hw_data(period, dir, mon)
	# Get baseline data
	baseline_data = filtered_data[0]
	before = baseline_data['hw'].values[0]
	# Get current data
	current_data = filtered_data[1]
	after = current_data['hw'].values[0]
	
	values = [before, after]
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
							html.Div(children=[
								html.Div(children=[
									html.H2(children='AVERAGE STREETCAR TRAVEL TIME', style={'margin-left':'0px'})
								], className='nine columns'),
								html.Div(children=[
									html.H3(children=AM_PEAK_LABEL),
									dash_components.StreetcarSpeeds( id='am-baseline-scs-table', data=filter_sc_table_data(9, 'AM')),
									dash_components.StreetcarSpeeds( id='am-scs-table', data=filter_sc_table_data(9, 'AM')),
									html.Div(dcc.Graph(id='am-tt-graph', figure=generate_sc_graph('AM')), style={'border-style':'solid', 'border-width': '1px'})
								], className='six columns'),
								html.Div(children=[
									html.H3(children=PM_PEAK_LABEL),
									dash_components.StreetcarSpeeds( id='pm-baseline-scs-table', data=filter_sc_table_data(9, 'PM')),
									dash_components.StreetcarSpeeds( id='pm-scs-table', data=filter_sc_table_data(9, 'PM')),
									html.Div(dcc.Graph(id='pm-tt-graph', figure=generate_sc_graph('PM')), style={'border-style':'solid', 'border-width': '1px'})
								], className='six columns')
							], className='nine columns', style={'margin-left':0}),
							html.Div(children=[
								html.Div(children=[
									html.H2(children='STREETCAR HEADWAY RELIABILITY', style={'margin-left':'0px'}),
									html.H4(children='% of streetcars within acceptable headway')
								], className='three columns'),
								html.Div(children=[
									html.Div(dcc.Graph(id='am-wb-schr-graph', figure=generate_schr_graph('AM', 'WB', 9))),
									html.Div(dcc.Graph(id='am-eb-schr-graph', figure=generate_schr_graph('AM', 'EB', 9)))
								], className='one-half columns'),
								html.Div(children=[
									html.Div(dcc.Graph(id='pm-wb-schr-graph', figure=generate_schr_graph('PM', 'WB', 9))),
									html.Div(dcc.Graph(id='pm-eb-schr-graph', figure=generate_schr_graph('PM', 'EB', 9)))
								], className='one-half columns')
							], className='three colums')
						], className='row'),
						dcc.RadioItems(
							id='streetcar-period-radio',
							options = [{'label': i, 'value': i} for i in TIME_PERIODS],
							value=TIME_PERIODS[0],
							className='radio-toolbar',
							labelStyle={'display': 'inline-block'}
						),
						dcc.RadioItems(
							id='streetcar-month-radio',
							options = [{'label': calendar.month_abbr[i], 'value': i} for i in MONTHS],
							value=MONTHS[0],
							className='radio-toolbar',
							labelStyle={'display': 'inline-block'}
						)]
					)]
# Car Tab
CAR_LAYOUT = [html.Div(children=[
				html.Div(children=[
					html.Div(children=[
						html.H2(children='CAR TRAVEL TIME', style={'margin-left':'0px'})
					], className='column'),
					html.Div(children=[
						html.H3(id='ctt-peak-label', children=AM_PEAK_LABEL),
						html.Div(dcc.Graph(id = STREETS[0] + '-tf-graph'),
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[1] + '-tf-graph'),
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[2] + '-tf-graph'),
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[3] + '-tf-graph'),
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[4] + '-tf-graph'),
								className='two columns'),
						html.Div(dcc.Graph(id = STREETS[5] + '-tf-graph'),
								className='two columns')
					], className='row', style={'padding-left':'2%'})
				]),
				html.Div(children=[
						html.H2(children='TRAFFIC VOLUMES', style={'margin-left':'0px'})
					], className='column'),
				html.Div(children=[
					html.Div(className='one columns'),
					html.Div(children=[
					dash_components.VolumeMap(id='volume-map', sl_data=json.loads(street_lines_df.to_json(orient='records')),
												ss_data=json.loads(street_segments_df.to_json(orient='records')),
												volume_data=filter_vol_data(9, 'AM'))
					], className='ten columns'),
					html.Div(className='one columns')
				], className='row'),
				dcc.RadioItems(
					id='car-period-radio',
					options = [{'label': i, 'value': i} for i in TIME_PERIODS],
					value=TIME_PERIODS[0],
					className='radio-toolbar',
					labelStyle={'display': 'inline-block'}
				),
				dcc.RadioItems(
					id='car-month-radio',
					options = [{'label': calendar.month_abbr[i], 'value': i} for i in MONTHS],
					value=MONTHS[0],
					className='radio-toolbar',
					labelStyle={'display': 'inline-block'}
				)]
			)]

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
	html.Link(
		rel='stylesheet',
		href='/src/css/components.css'
	),
	html.Div(children=[
		html.H1(children=TITLE, id='title')
	], className='row twelve columns'),
	dcc.Tabs(tabs=[{'label': 'Streetcars', 'value': 'streetcar'},
					{'label': 'Cars', 'value': 'car'}],
					value='streetcar', id='tabs', style={'font-weight':'bold'}),
	html.Div(id=MAIN_DIV, className='row', children=STREETCAR_LAYOUT), # Contents loaded via controllers. Default Streetcar tab.
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
@app.callback(
	Output('am-scs-table', 'data'),
	[Input('streetcar-month-radio', 'value')])
def update_am_scs_scstable(current_month):
	filtered_data = filter_sc_table_data(current_month, 'AM');
	return filtered_data

@app.callback(
	Output('pm-scs-table', 'data'),
	[Input('streetcar-month-radio', 'value')])
def update_pm_baseline_scstable(current_month):
	filtered_data = filter_sc_table_data(current_month, 'PM');
	return filtered_data

# Streetcar Headway Reliability controllers
@app.callback(
	Output('am-wb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_am_wb_schr_graph(current_month):
	figure = generate_schr_graph('AM', 'WB', current_month);
	return figure

@app.callback(
	Output('am-eb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_am_eb_schr_graph(current_month):
	figure = generate_schr_graph('AM', 'EB', current_month);
	return figure

@app.callback(
	Output('pm-wb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_pm_wb_schr_graph(current_month):
	figure = generate_schr_graph('PM', 'WB', current_month);
	return figure

@app.callback(
	Output('pm-eb-schr-graph', 'figure'),
	[Input('streetcar-month-radio', 'value')])
def update_pm_eb_schr_graph(current_month):
	figure = generate_schr_graph('PM', 'EB', current_month);
	return figure

################# Car tab ##########################################################################

# Car Travel Time graph controllers
@app.callback(
    Output('ctt-peak-label', 'children'),
    [Input('car-period-radio', 'value')])
def update_dundas(value):
	if value == 'AM':
		return AM_PEAK_LABEL
	elif value == 'PM':
		return PM_PEAK_LABEL

@app.callback(
    Output(STREETS[0] + '-tf-graph', 'figure'),
    [Input('car-period-radio', 'value')])
def update_dundas(value):
    return generate_tf_graph(STREETS[0], value)

@app.callback(
	Output(STREETS[1] + '-tf-graph', 'figure'),
    [Input('car-period-radio', 'value')])
def update_richmond(value):
    return generate_tf_graph(STREETS[1], value)	

@app.callback(
	Output(STREETS[2] + '-tf-graph', 'figure'),
    [Input('car-period-radio', 'value')])
def update_wellington(value):
	return generate_tf_graph(STREETS[2], value)

@app.callback(
    Output(STREETS[3] + '-tf-graph', 'figure'),
    [Input('car-period-radio', 'value')])
def update_queen(value):
    return generate_tf_graph(STREETS[3], value)

@app.callback(
    Output(STREETS[4] + '-tf-graph', 'figure'),
    [Input('car-period-radio', 'value')])
def update_adelaide(value):
    return generate_tf_graph(STREETS[4], value)

@app.callback(
    Output(STREETS[5] + '-tf-graph', 'figure'),
    [Input('car-period-radio', 'value')])
def update_front(value):
	# tf_graph = generate_tf_graph(STREETS[5], value)
	# tf_graph["layout"].showlegend = True
	# return tf_graph
	return generate_tf_graph(STREETS[5], value)

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
