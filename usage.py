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
car_df = pd.read_csv('car_travel_times.csv')
car_df['mon'] = [datetime.strptime(i, '%Y-%m-%d %H:%M:%S').date() for i in car_df['mon']]

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
								marker = dict(color = 'rgb(0,58,114)'), #bar color. Also accepts list of colors corresponding to each column
								width = .3)
								for street in STREETS} for period in ('AM', 'PM')}
AFTER_FIGS = {period : {street :go.Bar(
								x = car_df.loc[(car_df['corridor'] == street) & (car_df['mon'] >= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean().index,
								y = car_df.loc[(car_df['corridor'] == street) & (car_df['mon'] >= MIDDATE) & (car_df['time_period'] == period)].groupby(['dir'])['travel_time'].mean(),
								name = 'After',
								marker = dict(color = 'rgb(200,114,58)'), #bar color. Also accepts list of colors corresponding to each column
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

###################################################################################################
#                                                                                                 #
#                                         App Layout                                              #
#                                                                                                 #
###################################################################################################

# Streetcar graph
def generate_sc_graph(period):
	data = filter_sc_graph_data(period)
	layout = dict(xaxis = dict(title="Month"),
            yaxis = dict(title="Travel Time (min)"),
			autosize=True,
			height=250,
			margin=go.Margin(
				l=75,
				r=0,
				b=75,
				t=0,
				pad=4
			))
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
    layout = go.Layout(title = street, titlefont = dict(size = 20),
						xaxis = dict(title = 'Before/After', titlefont = dict(size = 15)),
						yaxis = dict(title = 'Travel Time', titlefont = dict( size = 15), range = YRNG),
						autosize = True,
						height = 250,
						margin=go.Margin(
									l=40,
									r=0,
									b=50,
									t=50,
									pad=4
								),
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
                                               size = 18,
                                               family = 'arial narrow')))
    if EB:
        layout['annotations'].append(dict(x = 'EB',
                                        y = YRNG[1],
                                        text = strdiffEB,
                                        xanchor = 'centre',
                                        yref = 'top',
                                        showarrow = False,
                                        font = dict(color = "black", size = 18, family = 'arial narrow')))
    return {'data' : [BEFORE_FIGS[period][street], AFTER_FIGS[period][street]], 'layout' : layout}
	
app = dash.Dash('')

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# main div contents
STREETCAR_LAYOUT = [html.Div(children=[
						html.Div(children=[
							html.H2(children='AVERAGE STREETCAR TRAVEL TIME'),
							html.Div(children=[
								html.H3(children=AM_PEAK_LABEL),
								dash_components.StreetcarSpeeds( id='am-baseline-scs-table', data=filter_sc_table_data(9, 'AM')),
								dash_components.StreetcarSpeeds( id='am-scs-table', data=filter_sc_table_data(9, 'AM')),
								html.Div(dcc.Graph(id='am-tt-graph', figure=generate_sc_graph('AM')), style={'border-style':'solid', 'border-width': '1px'})
							], className='four-half columns'),
							html.Div(children=[
								html.H3(children=PM_PEAK_LABEL),
								dash_components.StreetcarSpeeds( id='pm-baseline-scs-table', data=filter_sc_table_data(9, 'AM')),
								dash_components.StreetcarSpeeds( id='pm-scs-table', data=filter_sc_table_data(9, 'AM')),
								html.Div(dcc.Graph(id='pm-tt-graph', figure=generate_sc_graph('PM')), style={'border-style':'solid', 'border-width': '1px'})
							], className='four-half columns')
						]),
						dcc.RadioItems(
							id='streetcar-period-radio',
							options = [{'label': i, 'value': i} for i in TIME_PERIODS],
							value=TIME_PERIODS[0],
							labelStyle={'display': 'inline-block'}
						),
						dcc.RadioItems(
							id='streetcar-month-radio',
							options = [{'label': calendar.month_abbr[i], 'value': i} for i in MONTHS],
							value=MONTHS[0],
							labelStyle={'display': 'inline-block'}
						)]
					)]

CAR_LAYOUT = [html.Div(children=[
				html.Div(children=[
					html.H2(children='CAR TRAVEL TIME'),
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
					], className='row', style={'padding-left':'5%'})
				]),
				dcc.RadioItems(
                    id = 'car-period-radio',
                    options=[{'label' : timebucket, 'value' : timebucket} for timebucket in car_df['time_period'].unique()],
                    value = 'AM'
                )
			])]

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
		href='/src/css/SCStable.css'
	),
	html.Div(children=[
		html.H1(children=TITLE, id='title')
	], className='row twelve columns'),
	dcc.Tabs(tabs=[{'label': 'Streetcars', 'value': 'streetcar'},
					{'label': 'Cars', 'value': 'car'}],
					value='streetcar', id='tabs', style={'font-weight':'bold'}),
	html.Div(id=MAIN_DIV, className='row', children=STREETCAR_LAYOUT),
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

# Streetcar tab
	
@app.callback(
	dash.dependencies.Output('am-baseline-scs-table', 'data'),
	[dash.dependencies.Input('streetcar-period-radio', 'value'),
	 dash.dependencies.Input('streetcar-month-radio', 'value')])
def update_am_baseline_scstable(current_period, current_month):
	filtered_data = filter_sc_table_data(current_month, current_period);
	return filtered_data

@app.callback(
	dash.dependencies.Output('am-scs-table', 'data'),
	[dash.dependencies.Input('streetcar-period-radio', 'value'),
	 dash.dependencies.Input('streetcar-month-radio', 'value')])
def update_am_scs_scstable(current_period, current_month):
	filtered_data = filter_sc_table_data(current_month, current_period);
	return filtered_data

@app.callback(
	dash.dependencies.Output('pm-scs-table', 'data'),
	[dash.dependencies.Input('streetcar-period-radio', 'value'),
	 dash.dependencies.Input('streetcar-month-radio', 'value')])
def update_pm_baseline_scstable(current_period, current_month):
	filtered_data = filter_sc_table_data(current_month, current_period);
	return filtered_data

@app.callback(
	dash.dependencies.Output('pm-baseline-scs-table', 'data'),
	[dash.dependencies.Input('streetcar-period-radio', 'value'),
	 dash.dependencies.Input('streetcar-month-radio', 'value')])
def update_pm_scstable(current_period, current_month):
	filtered_data = filter_sc_table_data(current_month, current_period);
	return filtered_data

	
# Car tab
@app.callback(
    dash.dependencies.Output('ctt-peak-label', 'children'),
    [dash.dependencies.Input('car-period-radio', 'value')])
def update_dundas(value):
	if value == 'AM':
		return AM_PEAK_LABEL
	elif value == 'PM':
		return PM_PEAK_LABEL

@app.callback(
    dash.dependencies.Output(STREETS[0] + '-tf-graph', 'figure'),
    [dash.dependencies.Input('car-period-radio', 'value')])
def update_dundas(value):
    return generate_tf_graph(STREETS[0], value)

@app.callback(
    dash.dependencies.Output(STREETS[1] + '-tf-graph', 'figure'),
    [dash.dependencies.Input('car-period-radio', 'value')])
def update_queen(value):
    return generate_tf_graph(STREETS[1], value)

@app.callback(
    dash.dependencies.Output(STREETS[2] + '-tf-graph', 'figure'),
    [dash.dependencies.Input('car-period-radio', 'value')])
def update_adelaide(value):
    return generate_tf_graph(STREETS[2], value)

@app.callback(
    dash.dependencies.Output(STREETS[3] + '-tf-graph', 'figure'),
    [dash.dependencies.Input('car-period-radio', 'value')])
def update_front(value):
    return generate_tf_graph(STREETS[3], value)

@app.callback(
    dash.dependencies.Output(STREETS[4] + '-tf-graph', 'figure'),
    [dash.dependencies.Input('car-period-radio', 'value')])
def update_richmond(value):
    return generate_tf_graph(STREETS[4], value)

@app.callback(
    dash.dependencies.Output(STREETS[5] + '-tf-graph', 'figure'),
    [dash.dependencies.Input('car-period-radio', 'value')])
def update_wellington(value):
	return generate_tf_graph(STREETS[5], value)
	
if __name__ == '__main__':
    app.run_server(debug=True)
