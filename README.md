# King St. Pilot Public Dashboard
Dashboard for King Street Pilot for public viewing. This dashboard displays various traffic information pertaining to the King Street Pilot including streetcar/car travel times, and volumes using collect data. This dashboard is to be updated monthly.

Current Web App layout
![Streetcar Tab](https://github.com/CityofToronto/bdit_king_pilot_dashboard/blob/public-dashboard-layout/imgs/1.PNG "Streetcar Tab")

![Car Tab](https://github.com/CityofToronto/bdit_king_pilot_dashboard/blob/public-dashboard-layout/imgs/2.PNG "Car Tab")

## Features
- Visulized taffic volume for cars in the car volume map
- Bi-directional car travel times for each major EW road involved with the pilot
- Tables which tell the travel time and speeds of the King St. street cars
- Charts of the streetcar headway reliability percentages
- Graphs which visualize the travel times throughout the months of the pilot
- Period and Month filters that can alter the data of most of the components of the dashboard which the components dynamically update to
- Scalable components which allow usage of the dashboard on most screen sizes

## App Organization
The organization of this app is referenced from the [Internal Dashboard](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_v3) which is the internal version of the public dashboard. Please read the documentions of the Internal Dashboard as it closely relates to the app organization of the Public Dashboard.

The majority of the app is laid out in `usage.py` which is equivalent to the `app.py` in Dash Apps. This file is divided into 4 different sections being [`Constants`](#constants), [`Data Manipulation`](#data-manipulation), [`App Layout`](#app-layout), and [`Controllers`](#controllers).

### Constants
This is where global variables that are used in the app are placed. These constants are used to make modifications to the app easier. In addition, names of DIVs used in callbacks are stored in variables to reduce the risk of bugs.

### Data Manipulation
This is where the functions that are used to modify the loaded data for use in graphs and figures are stored. They are used in the callback functions whenever something is updated and to display the default values of the figures. 

### App Layout
Contains the functions that produce the graphs and figures with data from the data manipulation section. This section also contains the actual Dash HTML layout of the app where it is seperated into three sections.
- `STREETCAR_LAYOUT` contains all of the figures and graphs in the streetcar tab. This includes four streetcar speed tables, two dash graphs representing travel times throughout the study, and headway reliabilty graphs. These figures and graphs are fed data that is filtered by month.
- `CAR_LAYOUT` contains all of the figures and graphs in the car tab. This includes 6 graphs showing the peak travel times which represent the 6 major EW streets in the pilot and the volume map. These figures and graphs are filted by the period and month.
- `app.layout` is what is loaded onto the app initially. It features the web pages headers, tabs and footers. In addition, it also loads the stylesheets used in the app. The default `MAIN_DIV` loaded is `STREETCAR_LAYOUT`.

### Controllers
This section contains all of the callbacks which update the components of the page as the user changes tabs or applies a filter. Read more on [this Dash Tutorial](https://dev.to/alysivji/interactive-web-based-dashboards-in-python-5hf) on how these callbacks work. An example of a controller used in the app is shown below:
```
@app.callback(Output('main-page', 'children'), [Input('tabs', 'value')])
def display_content(value):
	if value == 'streetcar':
		return STREETCAR_LAYOUT
	elif value == 'car':
return CAR_LAYOUT
```
The controller listens to the HTML object with the `id` `'tabs'` and takes it's `'value'` whenever it changes. It then passes the `'value'` to the function immediately below. The result of the function is then passed to `'main-page'`'s `'children'`.

## Data
Currently the data used are from sample sets which are loaded from CSVs. In the future, the data will be loaded from the database [as done](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_v3#data) with the Internal Dashboard.

Data is currently loaded from CSVs using `pandas` and is stored in a dataframe.

## React Components
The Streetcar Speeds Table and Volume Map are both created and rendered in [React.js](https://reactjs.org/). Modifying the components in this repository will not cause changes to the Heroku web app as the components are being loaded from the [`bundle.js`](https://github.com/CityofToronto/bdit_king_pilot_dashboard/blob/public-dashboard-layout/dash_components/bundle.js) which was created after rendering the components in React. Please read the [documentation](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/dash_components) on reactifying these components as they were originally built in JS using `D3`.

For information on the components before they were reactified go to the [Volume Map Documentation](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/gh-pages/d3-volume_map) and the [original code](https://github.com/CityofToronto/bdit_king_pilot_dashboard/blob/gh-pages/d3-streetcar_speeds/index.html) for the streetcar speeds table.

## Styling
Styling is seperated into 3 different files and can be found [here](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/public-dashboard-layout/src/css). Each file serves a different purpose.
- `style.css` controls how the radio buttons are displayed in the web page. Only radios in the `radio-toolbar` class are affected.
- `dashboard.css` is the default stylesheet provided by Plot.ly for styling Dash. It has been modified slightly to accomodate styling of the dashboard.
- `components.css` is used to style the React components found [here](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/public-dashboard-layout/src/components).

The CSS stylesheets are loaded using:
```
@app.server.route('/src/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'src')
return send_from_directory(static_folder, path)
```
which was taken from [here](https://community.plot.ly/t/serve-locally-option-with-additional-scripts-and-style-sheets/6974/6).
The CSS stylesheets are then loaded into the HTML produced by Dash using:
```
html.Link(
		rel='stylesheet',
		href='/src/css/style.css'
)
```

## Deployment
The app is currently deployed on Heroku by detecting updates to this branch and automatically rebuilding the app. It is done similar to [this](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_v3#deployment). Ask @rdumas how he does it for this branch.

## Future Tasks
- Fix radio button layout as they are only their to test the filters
- Add animations to Plot.ly charts/graphs. Read the [tutorial](https://plot.ly/python/animations/) on how
- Finalize layout/styling of app
- Switch from mock data to real data using database connection
- Fix loading of Car tab. Currently the Car Travel Time graphs take a second to load which causes the height of the Div they are in to shift the page up when they load. (Not really important)
