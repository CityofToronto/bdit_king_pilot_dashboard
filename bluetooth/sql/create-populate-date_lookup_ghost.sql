DROP TABLE IF EXISTS king_pilot.date_lookup_ghost;

CREATE TABLE king_pilot.date_lookup_ghost AS (
SELECT
	dt.dt,
	CASE WHEN EXTRACT(isodow from dt) < 6 THEN 'Weekend' ELSE 'Weekday' END as day_type,
	'Ghost'::text as category
FROM 	(select dt::date from generate_series('2017-09-01', 
	'2018-12-31', '1 day'::interval) dt) dt);