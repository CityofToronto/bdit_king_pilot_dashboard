TRUNCATE king_pilot.tt_30min;

INSERT INTO king_pilot.tt_30min (bt_id, dt, time_bin, tt, obs)

SELECT 	A.bt_id, 
	B.datetime_bin::date AS dt,
	(TIMESTAMP WITHOUT TIME ZONE 'epoch' +
		INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time AS time_bin,
	SUM(B.tt*B.obs)/SUM(b.obs) AS tt,
	SUM(B.obs) AS obs

FROM king_pilot.bt_segments A
INNER JOIN bluetooth.aggr_5min B USING (analysis_id)
INNER JOIN king_pilot.date_baseline C USING (bt_id)

WHERE B.datetime_bin::date IN (C.dt) AND NOT (A.bt_id = 33 AND B.datetime_bin::date = '2017-09-19' AND B.datetime_bin::time >= '19:00')
GROUP BY A.bt_id, B.datetime_bin::date, C.day_type, (TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time
ORDER BY A.bt_id, B.datetime_bin::date, C.day_type, (TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time;