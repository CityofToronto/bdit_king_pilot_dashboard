from psycopg2 import connect
import pandas.io.sql as pandasql
import configparser
import dash
import dash_core_components as core
import dash_html_components as html
import plotly.graph_objs as go

CONFIG = configparser.ConfigParser()
CONFIG.read('C:\\Users\\rrodger\\reed.cfg')
dbset = CONFIG['DBSETTINGS']
con = connect(**dbset)

SQL = '''SELECT corridor, dir, mon, time_period, tt.tavel_time as travel_time
FROM dbs_travel_times tt
WHERE corridor = 'Dundas' '''

beforeafter = pandasql.read_sql(SQL, con)

fig1 = [go.Bar(x = beforeafter['dir'],
              y = beforeafter['travel_time'])]

app = dash.Dash()

app.layout = html.Div(children = [core.Graph(id='testGraph', figure = dict(data = fig1))])

if __name__ == '__main__':
    app.run_server(debug=True)
