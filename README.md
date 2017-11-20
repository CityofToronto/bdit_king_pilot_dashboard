# King St. Pilot Internal Dashboard
Dashboard for King St Pilot for internal management. This dashboard displays average travel times by timeperiod for streets parallel to King over the length of the pilot area.

## Deployment 
The app is currently deployed on Heroku by detecting updates to this branch and automatically rebuilding the app.
### Data
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

Data is synced after every timeperiod by the following shell script
```bash
curl -n -X DELETE https://api.heroku.com/apps/APP-ID/dynos -H "Content-Type: application/json" -H "Accept: application/vnd.heroku+json; version=3"
psql -h rds.ip -d bigdata -c "\COPY (SELECT * FROM king_pilot.dash_daily) TO STDOUT WITH (HEADER FALSE);" | psql     postgres://username:password@heroku.database.uri:5432/database -c "TRUNCATE king_pilot.dash_daily; COPY king_pilot.dash_daily FROM STDIN;"
```

The first line forces the heroku app to restart, thus killing all connections to the heroku PostgreSQL database, enabling the `TRUNCATE` and `COPY` operation to happen in the second line, which syncs the `dash_daily` table in heroku, with the `dash_daily` VIEW in our data warehouse.

## Contribution
This branch, now that it is in production, is **protected**. Develop instead on the [internal_dash_dev branch](https://github.com/CityofToronto/bdit_king_pilot_dashboard/tree/internal_dash_dev) and when an issue is complete, submit a pull request for staff to review.