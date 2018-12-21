CREATE OR REPLACE FUNCTION king_pilot.load_bt_data(
	)
    RETURNS integer
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$


BEGIN

	WITH aggr_5min AS (

		SELECT bt_id, 	rs.analysis_id,
		TIMESTAMP WITHOUT TIME ZONE 'epoch' +
		INTERVAL '1 second' * (floor((extract('epoch' from rs.measured_timestamp)-1) / 300) * 300) as datetime_bin,
		percentile_cont(0.5) WITHIN GROUP (ORDER BY rs.measured_time) AS travel_time,
		COUNT(rs.user_id) AS obs
	FROM bluetooth.raw_data rs
	JOIN bluetooth.class_of_device USING (cod)
	INNER JOIN king_pilot.bt_segments USING (analysis_id)
	WHERE rs.outlier_level = 0 AND device_class = 1 
		AND NOT (bt_id = 33 AND measured_timestamp::date = '2017-09-19' AND measured_timestamp::time >= '19:00')
	GROUP BY rs.analysis_id, datetime_bin
	)

	INSERT INTO king_pilot.tt_30min (bt_id, dt, time_bin, tt, obs)
	SELECT 	bt_id, 
		datetime_bin::date AS dt,
		(TIMESTAMP WITHOUT TIME ZONE 'epoch' +
			INTERVAL '1 second' * (floor((extract('epoch' from datetime_bin)) / 1800) * 1800))::time AS time_bin,
		SUM(tt*obs)/SUM(obs) AS tt,
		SUM(obs) AS obs
	FROM aggr_5min 
	GROUP BY bt_id, dt, time_bin;

	RETURN 1;
END

$BODY$;

ALTER FUNCTION king_pilot.load_bt_data()
    OWNER TO rdumas;

GRANT EXECUTE ON FUNCTION king_pilot.load_bt_data() TO bt_insert_bot;

REVOKE EXECUTE ON FUNCTION king_pilot.load_bt_data() FROM PUBLIC;

GRANT EXECUTE ON FUNCTION king_pilot.load_bt_data() TO aharpal;