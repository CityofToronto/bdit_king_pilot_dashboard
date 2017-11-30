import json
import os
from collections import OrderedDict

from dateutil.relativedelta import relativedelta
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from psycopg2 import connect
import pandas.io.sql as pandasql
import pandas as pd
import plotly.graph_objs as go

from dash_responsive import DashResponsive

from flask import send_from_directory

###################################################################################################
#                                                                                                 #
#                                       Data Fetching                                             #
#                                                                                                 #
###################################################################################################


database_url = os.getenv("DATABASE_URL")
if database_url is not None:
    con = connect(database_url)
else:
    import configparser
    CONFIG = configparser.ConfigParser()
    CONFIG.read('db.cfg')
    dbset = CONFIG['DBSETTINGS']
    con = connect(**dbset)

DATA = pandasql.read_sql('''SELECT street, direction, dt AS date, day_type, category, period, round(tt,1) tt, 
                         rank() OVER (PARTITION BY street, direction, day_type, period ORDER BY dt DESC) AS most_recent
                         FROM king_pilot.dash_daily''', con)
BASELINE = pandasql.read_sql('''SELECT street, direction, from_intersection, to_intersection, 
                             day_type, period, period_range, round(tt,1) tt 
                             FROM king_pilot.dash_baseline ''',
                             con)

con.close()

###################################################################################################
#                                                                                                 #
#                                        Constants                                                #
#                                                                                                 #
###################################################################################################


# Data management constants
STREETS = ['Dundas', 'Queen', 'Richmond', 'Adelaide', 'Wellington', 'Front']
DIRECTIONS = sorted(BASELINE['direction'].unique())
DATERANGE = [DATA['date'].min() - relativedelta(days=1),
             DATA['date'].max() + relativedelta(days=1)]
TIMEPERIODS = BASELINE[['day_type','period', 'period_range']].drop_duplicates().sort_values(['day_type', 'period_range'])
THRESHOLD = 1
MAX_TIME = 30 #Max travel time to fix y axis of graphs.

# Plot appearance
TITLE = 'King Street Transit Pilot: Vehicular Travel Time Monitoring'
BASELINE_LINE = {'color': 'rgba(128, 128, 128, 0.7)',
                 'width': 4}
PLOT = dict(margin={'t':10, 'b': 40, 'r': 40, 'l': 40, 'pad': 8})
PLOT_COLORS = dict(pilot='rgba(22, 87, 136, 100)',
                   baseline='rgba(128, 128, 128, 1.0)')
FONT_FAMILY = '"Open Sans", "HelveticaNeue", "Helvetica Neue", Helvetica, Arial, sans-serif'

# IDs for divs
STATE_DIV_ID = 'clicks-storage'
STREETNAME_DIV = ['street-name-'+str(i) for i in [0,1]]
SELECTED_STREET_DIV = 'selected-street'
TABLE_DIV_ID = 'div-table'
TIMEPERIOD_DIV = 'timeperiod'
CONTROLS = dict(timeperiods='timeperiod-radio',
                day_types='day-type-radio')
GRAPHS = ['eb_graph', 'wb_graph']


INITIAL_STATE = OrderedDict([(street,
                              dict(n_clicks=(1 if street == 'Dundas' else 0),
                                   clicked=(street == 'Dundas'))) for street in STREETS])

###################################################################################################
#                                                                                                 #
#                                   Data Manipulation                                             #
#                                                                                                 #
###################################################################################################

def deserialise_state(clicks_json):
    '''Turn the state stored in hidden div into python dict
    '''
    return json.loads(clicks_json, object_pairs_hook=OrderedDict)

def serialise_state(clicks_dict):
    '''Turn python dict of the clicks state of the table into json
    to store in hidden div
    '''
    return json.dumps(clicks_dict)

def pivot_order(df):
    '''Pivot the dataframe around street directions and order by STREETS global var
    '''
    if 'date' in df.columns:
        pivoted = df.pivot_table(index=['street', 'date'],
                                 columns='direction',
                                 values='tt').reset_index()
    else:
        pivoted = df.pivot_table(index='street', columns='direction', values='tt').reset_index()
    pivoted.street = pivoted.street.astype("category")
    pivoted.street.cat.set_categories(STREETS, inplace=True)
    return pivoted.sort_values(['street']).round(1)

def filter_table_data(period, day_type):
    '''Return data aggregated and filtered by period
    '''
    #current data
    filtered = DATA[(DATA['period'] == period) &
                    (DATA['day_type'] == day_type) &
                    (DATA['most_recent'] == 1)]

    pivoted = pivot_order(filtered)
    #baseline data
    
    filtered_base = BASELINE[(BASELINE['period'] == period) & (BASELINE['day_type'] == day_type)]
    pivoted_baseline = pivot_order(filtered_base)

    return (pivoted, pivoted_baseline)

def filter_graph_data(street, direction, day_type='Weekday', period='AMPK'):
    '''Filter dataframes by street, direction, day_type, and period
    Returns a filtered baseline, and a filtered current dataframe
    '''
    filtered = DATA[(DATA['street'] == street) &
                    (DATA['period'] == period) &
                    (DATA['day_type'] == day_type) &
                    (DATA['direction'] == direction)]
    filtered_baseline = BASELINE[(BASELINE['street'] == street) &
                                 (BASELINE['period'] == period) &
                                 (BASELINE['day_type'] == day_type) &
                                 (BASELINE['direction'] == direction)]
    return (filtered, filtered_baseline)

###################################################################################################
#                                                                                                 #
#                                         App Layout                                              #
#                                                                                                 #
###################################################################################################

def generate_row_class(clicked):
    '''Assigns class to clicked row'''
    if clicked:
        return 'selected'
    else:
        return 'notselected'
    
def intstr(integer):
    if integer > 0:
        return str(integer)
    else:
        return integer

def generate_direction_cells(before, after):
    '''Generate before/after cells for each street direction
    '''
    return [html.Td(intstr(after), className=after_cell_class(before, after)),
            html.Td(intstr(before), className='baseline')]

def after_cell_class(before, after):
    '''Colour the after cell based on its difference with the before
    '''
    if after - before > THRESHOLD:
        return 'worse'
    elif after - before < -THRESHOLD:
        return 'better'
    else:
        return 'same'

def generate_row(df_row, baseline_row, row_state):
    """Create an HTML row from a database row (each street)

        :param df_row: 
            Daily data dataframe row
        :param baseline_row: 
            Baseline row for that street
        :param row_state: 
            Current state of that row: number of clicks, whether it is currently clicked
    """
    return html.Tr([html.Td(df_row['street'], className='segname'),
                    *generate_direction_cells(baseline_row[DIRECTIONS[0]], df_row[DIRECTIONS[0]]),
                    *generate_direction_cells(baseline_row[DIRECTIONS[1]], df_row[DIRECTIONS[1]])],
                   id=df_row['street'],
                   className=generate_row_class(row_state['clicked']),
                   n_clicks=row_state['n_clicks'])

def generate_table(state, day_type, period):
    """Generate HTML table of streets and before-after values
    
        :param state: 
            Dictionary of table's state: {street: (n_clicks, clicked)}
        :param day_type: 
            Type of day
        :param period: 
            Timeperiod name
    """

    filtered_data, baseline = filter_table_data(period, day_type)
    #Current date for the data, to replace "After" header
    day = filtered_data['date'].iloc[0].strftime('%a %b %d')
                       
    return html.Table([html.Tr([html.Td(""), html.Td("Eastbound", colSpan=2), html.Td("Westbound", colSpan=2)])] +
                      [html.Tr([html.Td(""), html.Td(day), html.Td("Baseline"), html.Td(day), html.Td("Baseline")])] +
                      # Generate a row 
                      [generate_row(new_row[1], baseline_row[1], row_state)
                      # for each street, keeping in mind the state (which row is clicked)
                       for new_row, baseline_row, row_state
                       in zip(filtered_data.iterrows(),
                              baseline.iterrows(),
                              state.values())]
                      , id='data_table')

def generate_graph(street, direction, day_type='Weekday', period='AMPK'):
    '''Generate a Dash bar chart of average travel times by day
    '''
    after_data, base_data = filter_graph_data(street, direction, day_type, period)
    if after_data.empty:
        data = [go.Bar()]
        line = None
        annotations = None
    else:
        baseline_days = after_data[after_data['category'] == 'Baseline']
        if baseline_days.empty:
            data = [go.Bar(x=after_data['date'],
                           y=after_data['tt'],
                           text=after_data['tt'].round(),
                           hoverinfo='x+y',
                           textposition='inside',
                           insidetextfont=dict(color='rgba(255,255,255,1)',
                                               size=12),
                           marker=dict(color=PLOT_COLORS['pilot']))]
        else:
            pilot_days = after_data[after_data['category'] == 'Pilot']
            pilot_data = dict(x=pilot_days['date'],
                              y=pilot_days['tt'],
                              text=pilot_days['tt'].round(),
                              hoverinfo='x+y',
                              textposition='inside',
                              insidetextfont=dict(color='rgba(255,255,255,1)',
                                                  size=12),
                              marker=dict(color=PLOT_COLORS['pilot']),
                              type='bar',
                              name='Pilot')
            baseline_data = dict(x=baseline_days['date'],
                                 y=baseline_days['tt'],
                                 text=baseline_days['tt'].round(),
                                 hoverinfo='x+y',
                                 textposition='inside',
                                 insidetextfont=dict(color='rgba(255,255,255,1)',
                                                     size=12),
                                 marker=dict(color=PLOT_COLORS['baseline']),
                                 type='bar',
                                 name='Baseline')
            data = [baseline_data, pilot_data]
        annotations = [dict(x=-0.008,
                            y=base_data.iloc[0]['tt'] + 2,
                            text='Baseline',
                            font={'color':BASELINE_LINE['color']},
                            xref='paper',
                            yref='yaxis',
                            showarrow=False
                            )]
        line = {'type':'line',
                'x0': 0,
                'x1': 1,
                'xref': 'paper',
                'y0': base_data.iloc[0]['tt'],
                'y1': base_data.iloc[0]['tt'],
                'line': BASELINE_LINE
               }
    layout = dict(font={'family': FONT_FAMILY},
                  autosize=True,
                  height=225,
                  barmode='relative',
                  xaxis=dict(title='Date',
                             range=DATERANGE,
                             fixedrange=True),
                  yaxis=dict(title='Travel Time (min)',
                             range=[0, MAX_TIME],
                             fixedrange=True),
                  shapes=[line],
                  margin=PLOT['margin'],
                  annotations=annotations,
                  legend={'xanchor':'right'}
                  )
    return {'layout': layout, 'data': data}

app = DashResponsive()
app.config['suppress_callback_exceptions'] = True
app.title=TITLE
server = app.server

server.secret_key = os.environ.get('SECRET_KEY', 'my-secret-key')
            
app.layout = html.Div([

html.Link(rel = 'stylesheet',
              href = '/css/dashboard.css'),
html.Link(rel = 'stylesheet',
              href = '/css/style.css'),
          
html.Div(children=[html.H1(children=TITLE, id='title'),
                  ], className='row twelve columns'),
    html.Div([
        html.Div(children=[
            html.H2(id=TIMEPERIOD_DIV, children='Weekday AM Peak'),
            html.Div(id=TABLE_DIV_ID, children=generate_table(INITIAL_STATE, 'Weekday', 'AM Peak')),
            html.Div([html.B('Travel Time', style={'background-color':'#E9A3C9'}),
                      ' 1+ min', html.B(' longer'), ' than baseline']),
            html.Div([html.B('Travel Time', style={'background-color':'#A1D76A'}),
                      ' 1+ min', html.B(' shorter'), ' than baseline']),
            dcc.RadioItems(id=CONTROLS['timeperiods'],
                           value=TIMEPERIODS.iloc[0]['period'],
                           className='radio-toolbar'),
            dcc.RadioItems(id=CONTROLS['day_types'],
                           options=[{'label': day_type,
                                     'value': day_type,
                                     'id': day_type} 
                                     for day_type in TIMEPERIODS['day_type'].unique()],
                           value=TIMEPERIODS.iloc[0]['day_type'],
                           className='radio-toolbar')
                           ],
                 className='four columns'
                ),
        html.Div(children=[
            html.H2(id=STREETNAME_DIV[0], children=[html.B('Dundas Eastbound:'), ' Bathurst - Jarvis']),
            dcc.Graph(id=GRAPHS[0],
                      figure=generate_graph(STREETS[0], DIRECTIONS[1]),
                      config={'displayModeBar': False}),
            html.H2(id=STREETNAME_DIV[1], children=[html.B('Dundas Westbound:'), ' Jarvis - Bathurst']),
            dcc.Graph(id=GRAPHS[1],
                      figure=generate_graph(STREETS[0], DIRECTIONS[1]),
                      config={'displayModeBar': False})], 
                      
                      className='eight columns'),
    ], className='row'),
    html.Div(children=html.H3(['Created by the ',
                               html.A('Big Data Innovation Team',
                                      href="https://www1.toronto.ca/wps/portal/contentonly?vgnextoid=f98b551ed95ff410VgnVCM10000071d60f89RCRD")],
                                      style={'text-align':'right', 'padding-right':'1em'}),
             className='row'),
    html.Div(id=STATE_DIV_ID, style={'display': 'none'}, children=serialise_state(INITIAL_STATE)),
    html.Div(id=SELECTED_STREET_DIV, style={'display': 'none'}, children=[STREETS[0]])
])

#CSS

app.css.config.serve_locally= True
app.scripts.config.serve_locally = True

@app.server.route('/css/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'css')
    return send_from_directory(static_folder, path)


#==============================================================================
# app.css.append_css({
#     'external_url': 'https://cityoftoronto.github.io/bdit_king_pilot_dashboard/css/dashboard.css'
# })
# app.css.append_css({
#     'external_url': 'https://cityoftoronto.github.io/bdit_king_pilot_dashboard/css/style.css'
# })
#==============================================================================

###################################################################################################
#                                                                                                 #
#                                         Controllers                                             #
#                                                                                                 #
###################################################################################################


@app.callback(Output(CONTROLS['timeperiods'], 'options'),
              [Input(CONTROLS['day_types'], 'value')])
def generate_radio_options(day_type='Weekday'):
    '''Assign time period radio button options based on select day type
    '''
    return [{'label': period, 'value': period}
            for period
            in TIMEPERIODS[TIMEPERIODS['day_type'] == day_type]['period']]

@app.callback(Output(CONTROLS['timeperiods'], 'value'),
              [Input(CONTROLS['day_types'], 'value')])
def assign_default_timperiod(day_type='Weekday'):
    '''Assign the time period radio button selected option based on selected day type
    '''
    return TIMEPERIODS[TIMEPERIODS['day_type'] == day_type].iloc[0]['period']

@app.callback(Output(TABLE_DIV_ID, 'children'),
              [Input(CONTROLS['timeperiods'], 'value'),
               Input(CONTROLS['day_types'], 'value')],
              [State(STATE_DIV_ID, 'children')])
def update_table(period, day_type, state_data):
    '''Generate HTML table of before-after travel times based on selected
    day type, time period, and remember which row was previously selected
    '''
    state_data_dict = deserialise_state(state_data)
    table = generate_table(state_data_dict, day_type, period)
    return table


def create_row_click_function(streetname):
    '''Create a callback function for a given streetname
    streetname is the id for the row in the datatable

    '''
    @app.callback(Output(streetname, 'className'),
                  [Input(SELECTED_STREET_DIV, 'children')])
    def update_clicked_row(street):
        '''Inner function to update row with id=streetname
        '''
        if street:
            return generate_row_class(streetname == street[0])
        else:
            return generate_row_class(False)
    update_clicked_row.__name__ = 'update_row_'+streetname
    return update_clicked_row

[create_row_click_function(key) for key in INITIAL_STATE.keys()]

@app.callback(Output(STATE_DIV_ID, 'children'),
              [Input(street, 'n_clicks') for street in STREETS],
              [State(STATE_DIV_ID, 'children'),
               State(SELECTED_STREET_DIV, 'children')])
def row_click(*args):
    '''Detect which row was clicked and update the graphs to be for the selected street

    Clicks are detected by comparing the previous number of clicks for each row with
    the current state. Previous state is stored in a json in a hidden div
    '''
    rows, old_clicks, prev_clicked_street = args[:-1], args[-2], args[-1]
    clicks = deserialise_state(old_clicks)
    click_updated = False
    for click_obj, n_click_new in zip(clicks.values(), rows):
        if n_click_new > click_obj['n_clicks']:
            click_obj['clicked'] = True
            click_obj['n_clicks'] = n_click_new
            click_updated = True
        else:
            click_obj['clicked'] = False
    #If no street was found to be clicked by this function, revert to previously clicked street.
    if not click_updated:
        clicks[prev_clicked_street[0]]['clicked'] = True
    return serialise_state(clicks)

@app.callback(Output(SELECTED_STREET_DIV, 'children'),
              [Input(STATE_DIV_ID, 'children')])
def update_selected_street(state_data):
    '''Store selected street in a hidden div based on current state as
    stored in its own hidden div
    '''
    state_data_dict = deserialise_state(state_data)
    return [street for street, click_obj in state_data_dict.items() if click_obj['clicked']]

def create_update_street_name(dir_id):
    @app.callback(Output(STREETNAME_DIV[dir_id], 'children'),
                  [Input(SELECTED_STREET_DIV, 'children')])
    def update_street_name(street):
        try:
            from_to = BASELINE[(BASELINE['street'] == street[0]) &
                               (BASELINE['direction'] == DIRECTIONS[dir_id])][['from_intersection',
                                                                               'to_intersection']].iloc[0]
        except IndexError:
            return [html.B(street[0]+': ')]
        else:
            return [html.B(street[0] + ' ' + DIRECTIONS[dir_id] + ': '),
                    from_to['from_intersection'] + ' - ' + from_to['to_intersection']]

[create_update_street_name(i) for i in [0,1]]

def create_update_graph(graph_number):
    '''Dynamically create callback functions to update graphs based on a graph number
    '''
    @app.callback(Output(GRAPHS[graph_number], 'figure'),
                  [Input(SELECTED_STREET_DIV, 'children'),
                   Input(CONTROLS['timeperiods'], 'value'),
                   Input(CONTROLS['day_types'], 'value')])
    def update_graph(street, period, day_type):
        '''Update the graph for a street direction based on the selected:
         - street
         - time period
         - day type
        '''
        return generate_graph(street[0], DIRECTIONS[graph_number], period=period, day_type=day_type)
    update_graph.__name__ = 'update_graph_' + GRAPHS[graph_number]
    return update_graph

[create_update_graph(i) for i in range(len(GRAPHS))]

@app.callback(Output(TIMEPERIOD_DIV, 'children'),
              [Input(CONTROLS['timeperiods'], 'value'),
               Input(CONTROLS['day_types'], 'value')])
def update_timeperiod(timeperiod, day_type):
    '''Update sub title text based on selected time period and day type
    '''
    time_range = TIMEPERIODS[(TIMEPERIODS['period'] == timeperiod) & (TIMEPERIODS['day_type'] == day_type)].iloc[0]['period_range']
    return day_type + ' ' + timeperiod + ' ' + time_range


if __name__ == '__main__':
    app.run_server(debug=True)

