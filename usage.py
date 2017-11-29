import dash_components
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import calendar

df = pd.read_csv('streetcar_travel_times.csv')

#periods
time_periods = ['AM', 'PM']

#months
months = pd.to_datetime(df['mon']).map(lambda t: t.date().month).unique()

app = dash.Dash('')

app.scripts.config.serve_locally = True

app.layout = html.Div([
	dash_components.StreetcarSpeeds( id='streetcarspeeds'),
    dcc.RadioItems(
		id='period_radio',
		options = [{'label': i, 'value': i} for i in time_periods],
		value=time_periods[0],
		labelStyle={'display': 'inline-block'}
	),
	dcc.RadioItems(
		id='month_radio',
		options = [{'label': calendar.month_abbr[i], 'value': i} for i in months],
		value=months[0],
		labelStyle={'display': 'inline-block'}
	)
])

# Update StreetCarSpeeds table when period_radio or month_radio value changes
@app.callback(
	dash.dependencies.Output('streetcarspeeds', 'data'),
	[dash.dependencies.Input('period_radio', 'value'),
	 dash.dependencies.Input('month_radio', 'value')])
def update_scstable(current_period, current_month):
	tt_subset = df[(pd.to_datetime(df['mon']).map(lambda t: t.date().month)==current_month) & (df['time_period']==current_period)]
	return {
		'data': tt_subset.to_json(orient='records')
	}

if __name__ == '__main__':
    app.run_server(debug=True)
