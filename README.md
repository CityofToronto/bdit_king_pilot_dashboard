# King St. Pilot Public Dashboard
Dashboard for King Street Pilot for public viewing. This dashboard displays various traffic information pertaining to the King Street Pilot including streetcar/car travel times, and volumes using collect data. This dashboard is to be updated monthly.

## App Organization
The organization of this app is referenced from the [Internal Dashboard](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_v3) which is the internal version of the public dashboard. Please read the documentions of the Internal Dashboard as it closely relates to the app organization of the Public Dashboard.

The majority of the app is laid out in `usage.py` which is equivalent to the `app.py` in Dash Apps. This file is divided into 4 different sections being `Constants`, `Data Manipulation`, `App Layout`, and `Controllers`.

### Constants
This is where global variables that are used in the app are placed. These constants are used to make modifications to the app easier. In addition, names of DIVs used in callbacks are stored in variables to reduce the risk of bugs.

### Data Manipulation
This is where the functions that are used to modify the loaded data for use in graphs and figures. 

### App Layout
Contains the functions that produce the graphs and figures with data from the data manipulation section. This section also contains the actual Dash HTML layout of the app where it is seperated into three sections.
- `STREETCAR_LAYOUT` contains all of the figures and graphs in the streetcar tab. This includes four streetcar speed tables, two dash graphs representing travel times throughout the study, and headway reliabilty graphs. These figures and graphs are fed data that is filtered by month.
- `CAR_LAYOUT` contains all of the figures and graphs in the car tab. This includes 6 graphs showing the peak travel times which represent the 6 major EW streets in the pilot and the volume map. These figures and graphs are filted by the period and month.
- `app.layout` is what is loaded onto the app initially. It features the web pages headers, tabs and footers. In addition, it also loads the stylesheets used in the app. The default `MAIN_DIV` loaded is `STREETCAR_LAYOUT`.

### Controllers
This section contains all of the callbacks which update the components of the page as the user changes tabs or applies a filter. Read more on [this Dash Tutorial](https://dev.to/alysivji/interactive-web-based-dashboards-in-python-5hf) on how these callbacks work.

## Data
Currently the data used are from sample sets which are loaded from CSVs. In the future, the data will be loaded from the database [as done](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_v3#data) with the Internal Dashboard.

## React Components
The Streetcar Speeds Table and Volume Map are both created and rendered in [React.js](https://reactjs.org/). Please read the [documentation](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/dash_components) on reactifying these components as they were originally built in JS using `D3`.
- [Volume Map Documentation](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/gh-pages/d3-volume_map)

## Deployment
The app is currently deployed on Heroku by detecting updates to this branch and automatically rebuilding the app. It is done similar to [this](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_v3#deployment). Ask @rdumas how he does it for this branch.

