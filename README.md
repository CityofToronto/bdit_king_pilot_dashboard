# King St. Pilot Internal Dashboard
Dashboard for King St Pilot for internal management. This dashboard displays average travel times by timeperiod for streets parallel to King over the length of the pilot area.

## App Organization

The layout of the code is inspired by the Model-View-Controller paradigm, specifically from [this Dash tutorial](https://dev.to/alysivji/interactive-web-based-dashboards-in-python-5hf). In addition, parameters and constants that someone would want to change when forking this are frontloaded in ALL_CAPS variables, in order to make modification easier. The names of DIVs used in callbacks are also stored in variables in order to reduce the risk of bugs since variable names are linted to see if they exist.

In addition to some of the plot styling being in these variables, [two css stylesheets](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/gh-pages/css) are loaded from the `gh-pages` branch to style the table and buttons. For... reasons, these can't be loaded from local files ¯\_(ツ)_/¯.

### Other thing to note

In order to add the "viewport" html `meta` tag to the `<head>` of the page, `dash.Dash` had to subclassed and its `index()` method overwritten, this class is stored in `dash_responsive.py`. 

#### Detecting row clicks

Dash detects the number of clicks any html element has received. By storing all these in a "state" variable, one can compare previous and current state to determine which object was clicked. This is handled by the `row_click` function, which is fired when the number of clicks changes for any row (a Dash input), and also the previous state, and previously clicked row. Because [modifying global variables is **bad news** in Dash](https://plot.ly/dash/sharing-data-between-callbacks), these two states are serialized to json and stored in a hidden html div.

When a row is clicked:
1. the `row_click` function compares the current number of clicks for each row with the previous state and then labels the row for which this changed as "clicked". 
2. the `row_click` function updates the `STATE_DIV_ID` with the number of clicks and the row which is clicked.
3. this triggers updating the `SELECTED_STREET_DIV`
4. which triggers updating the selected rows classes to add or remove the "selected" class.

#### Creating multiple similar callbacks

Yes, you can put callback/function creation in a loop to iterate over, for example, every street. You just have to define an outer function that creates these callbacks, for example:

```python
def create_row_click_function(streetname):
    
    @app.callback(Output(streetname, 'className'),
                  [Input(SELECTED_STREET_DIV, 'children')])
    def update_clicked_row(street):
        if street:
            return generate_row_class(streetname == street[0])
        else:
            return generate_row_class(False)
    update_clicked_row.__name__ = 'update_row_'+streetname
    return update_clicked_row

#and then call the outer function in a loop
[create_row_click_function(key) for key in INITIAL_STATE.keys()]
```

### Data
Data from downtown Bluetooth detectors arrives in our database after initial filtering by bliptrack. 

There it is grouped into five-minute-bins using the median to reduce the impact of extreme outliers.

The five-minute bins are grouped again into 30-minute bins using weighted average by the number of observations per five-minute-bin and separated by working day and nonworking day. 

The 30-minute data collected before the pilot was plotted as scatterplots and quality checked. Major outliers were noted and removed from the baseline if deemed necessary. 
For example on Queen Street, a major slowdown was identified at midnight, which had a major impact on the baseline. This was due to Nuit Blanche so Queen University to Yonge was listed to have September 30th and October 1st removed from its baseline.

The dates and segments that were removed are: 

1. Queen EB University to Yonge: 2017-09-24, 2017-09-30, 2017-10-01
2. Queen WB Yonge to University: 2017-09-30, 2017-10-01
3. Queen WB Spadina to Bathurst: 2017-09-19
4. Adelaide EB Jarvis to Parliament: 2017-10-30, 2017-10-31, 2017-11-01
5. Front EB Jarvis to Parliament: 2017-09-16
6. Dufferin SB Queen to King: 2017-11-05
7. Jarvis NB Front to King: 2017-09-16
8. Jarvis NB King to Queen: 22017-09-17
9. Parliament NB Queen to Dundas: 2017-09-24

The 30-minute data was then aggregated by time period, and pre-pilot data were averaged to get a baseline for a given period during the weekend or week.
This visualization depends on two tables, which are views in the data warehouse: 

 - Baseline travel times for each (street, direction, day type, timeperiod)  ([source](https://github.com/CityofToronto/bdit_king_pilot_dashboard/blob/data_pipeline/bluetooth/sql/create-view-dash_baseline.sql))
 - Daily travel times for each (street, direction, day type, timeperiod) ([source](https://github.com/CityofToronto/bdit_king_pilot_dashboard/blob/data_pipeline/bluetooth/sql/create-view-dash_daily.sql))

Where day type is one of [Weekday, Weekend], and the time periods depend on the day type.

This code automatically connects to the database: either our local data warehouse or the heroku postgresql database. 

```python
database_url = os.getenv("DATABASE_URL")
if database_url is not None:
    con = connect(database_url)
else:
    import configparser
    CONFIG = configparser.ConfigParser()
    CONFIG.read('db.cfg')
    dbset = CONFIG['DBSETTINGS']
    con = connect(**dbset)
```

## Deployment 
The app is currently deployed on Heroku by detecting updates to this branch and automatically rebuilding the app.

### Data

Data is synced after every timeperiod by the following shell script
```bash
curl -n -X DELETE https://api.heroku.com/apps/APP-ID/dynos -H "Content-Type: application/json" -H "Accept: application/vnd.heroku+json; version=3"
psql -h rds.ip -d bigdata -c "\COPY (SELECT * FROM king_pilot.dash_daily) TO STDOUT WITH (HEADER FALSE);" | psql     postgres://username:password@heroku.database.uri:5432/database -c "TRUNCATE king_pilot.dash_daily; COPY king_pilot.dash_daily FROM STDIN;"
```

The first line forces the heroku app to restart, thus killing all connections to the heroku PostgreSQL database, enabling the `TRUNCATE` and `COPY` operation to happen in the second line, which syncs the `dash_daily` table in heroku, with the `dash_daily` VIEW in our data warehouse.

## Contribution
This branch, now that it is in production, is **protected**. Develop instead on the [internal_dash_dev branch](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_dev) and when an issue is complete, submit a pull request for staff to review.
