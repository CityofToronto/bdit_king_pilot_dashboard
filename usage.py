import dash_components
import dash
import dash_html_components as html

app = dash.Dash('')

app.scripts.config.serve_locally = True

app.layout = html.Div([
    dash_components.ExampleComponent( id='input' ),
    html.Div(id='output')
])

@app.callback(
	dash.dependencies.Output('output', 'children'),
	[dash.dependencies.Input('input', 'id')])
def display_output(value):
    return 'You have entered {}'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
