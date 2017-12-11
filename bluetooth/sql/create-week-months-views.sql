CREATE OR REPLACE VIEW king_pilot.pilot_weeks AS
SELECT week, row_number() OVER() as week_number 
                            FROM (SELECT DISTINCT ON(date_trunc('week', dt)::DATE) date_trunc('week', dt)::DATE as week
                          FROM king_pilot.dash_daily_dev
                          WHERE dt >= '2017-11-13' )a
                          ORDER BY week;

CREATE OR REPLACE VIEW king_pilot.pilot_months AS
SELECT month, row_number() OVER() as month_number 
                            FROM (SELECT DISTINCT ON(date_trunc('month', dt)::DATE) date_trunc('month', dt)::DATE as month
                          FROM king_pilot.dash_daily
                          WHERE dt >= '2017-11-13' )a
                          ORDER BY month;