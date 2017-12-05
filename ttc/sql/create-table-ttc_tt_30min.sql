DROP TABLE IF EXISTS king_pilot.ttc_tt_30min;

CREATE TABLE king_pilot.ttc_tt_30min (
	bt_id int,
	dt date,
	time_bin time without time zone,
	tt int,
	obs int);

INSERT INTO king_pilot.ttc_tt_30min (bt_id, dt, time_bin, tt, obs)

SELECT 	bt_id, 
	end_dt::date AS dt,
	(TIMESTAMP WITHOUT TIME ZONE 'epoch' +
		INTERVAL '1 second' * (floor((extract('epoch' from end_dt)) / 1800) * 1800))::time AS time_bin,
	AVG(tt_sec) AS tt,
	COUNT(*) AS obs

FROM king_pilot.bt_ttc_tt

GROUP BY bt_id, end_dt::date, (TIMESTAMP WITHOUT TIME ZONE 'epoch' +INTERVAL '1 second' * (floor((extract('epoch' from end_dt)) / 1800) * 1800))::time
ORDER BY bt_id, end_dt::date, (TIMESTAMP WITHOUT TIME ZONE 'epoch' +INTERVAL '1 second' * (floor((extract('epoch' from end_dt)) / 1800) * 1800))::time;