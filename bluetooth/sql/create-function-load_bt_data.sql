CREATE OR REPLACE FUNCTION king_pilot.load_bt_data() RETURNS integer AS $$

BEGIN
	-- TRANSFER bluetooth.raw_data TO bluetooth.observations
	INSERT INTO bluetooth.observations (user_id,analysis_id,
	  measured_time,
	  measured_time_no_filter,
	  startpoint_number,
	  startpoint_name,
	  endpoint_number,
	  endpoint_name,
	  measured_timestamp,
	  outlier_level,
	  cod,
	  device_class)
	SELECT * FROM bluetooth.raw_data rs;

	-- LOAD bluetooth.aggr_5min with new data
	INSERT INTO bluetooth.aggr_5min (analysis_id, datetime_bin, tt, obs)
	SELECT	rs.analysis_id,
		TIMESTAMP WITHOUT TIME ZONE 'epoch' +
		INTERVAL '1 second' * (floor((extract('epoch' from rs.measured_timestamp)-1) / 300) * 300) as datetime_bin,
		median(rs.measured_time) AS travel_time,
		COUNT(rs.user_id) AS obs
	FROM bluetooth.raw_data rs
	WHERE rs.outlier_level = 0 AND device_class = 1
	GROUP BY rs.analysis_id, (floor((extract('epoch' from rs.measured_timestamp)-1) / 300) * 300)
	ORDER BY rs.analysis_id, (floor((extract('epoch' from rs.measured_timestamp)-1) / 300) * 300);

	-- TRUNCATE king_pilot.tt_30min
	TRUNCATE king_pilot.tt_30min;

	-- LOAD king_pilot.30min
	INSERT INTO king_pilot.tt_30min (bt_id, dt, time_bin, tt, obs)
	SELECT 	A.bt_id, 
		B.datetime_bin::date AS dt,
		(TIMESTAMP WITHOUT TIME ZONE 'epoch' +
			INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time AS time_bin,
		SUM(B.tt*B.obs)/SUM(b.obs) AS tt,
		SUM(B.obs) AS obs
	FROM king_pilot.bt_segments A
	INNER JOIN bluetooth.aggr_5min B USING (analysis_id)
	WHERE NOT (A.bt_id = 33 AND B.datetime_bin::date = '2017-09-19' AND B.datetime_bin::time >= '19:00')
	GROUP BY A.bt_id, B.datetime_bin::date, (TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time
	ORDER BY A.bt_id, B.datetime_bin::date,  (TIMESTAMP WITHOUT TIME ZONE 'epoch' + INTERVAL '1 second' * (floor((extract('epoch' from B.datetime_bin)) / 1800) * 1800))::time;

	RETURN 1;
END
$$ LANGUAGE plpgsql;